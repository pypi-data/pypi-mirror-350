from django.conf import settings
from ardhi_framework.interservice import get_land_admin_ingestion_parcels, get_parcel_invoices_status, \
    registration_property_details, survey_details
from ardhi_framework.property_processing.snitch import snitch_func
from ardhi_framework.property_processing.transaction_configs import get_config


class UsefulFunctionsClass:

    def __init__(self) -> None:
        pass

    """Response formatter"""

    def _(self, func_):
        is_fine, info = func_()
        if not is_fine:
            raise ValueError(info)
        return is_fine, info

    """Return readable text"""

    def _r(self, obj):
        if isinstance(obj, str):
            return obj.replace("_", " ").replace("-", " ").title()
        if isinstance(obj, list):
            # recur through list
            text = [self._r(el) for el in obj]
            return ", ".join(text)
        try:
            return self._r(str(obj))
        except:
            return '**'

    """Keys checker, value in dict"""

    def _check_vals(self, name: str, obj: dict, query: list[dict]):
        """ dict: {
        'key': ['val', 'err'],
        }"""
        if not obj:
            return False, f'Validation process for {name} failed'
        for item in query:
            for k, v in item.items():
                if obj.get(k, None) != v[0]:
                    return False, self._r(v[1])
        return True, 'Valid objects'


class TransactableParcel(UsefulFunctionsClass):
    def __init__(self, parcel_number, context, configurations=None, **kwargs):
        super().__init__()
        self.active_ownership = None
        self.property_router: dict = None
        self.property_instance: dict = None
        self.parcel_number = parcel_number.upper().replace(" ", "")
        self.configs = configurations if bool(configurations) else get_config(kwargs.get('process_name'))
        self.nature_of_title = kwargs.get("nature_of_title") or None
        self.context = context
        self.property_reg_details = {}
        self.readable_nature_of_title = ""
        self.validate = True

    @staticmethod
    def false_res(msg):
        return False, f"{msg}"

    def true_res(self, msg):
        return True, {
            "details": msg,
            "parcel_number": self.parcel_number,
            "nature_of_title": self.nature_of_title,
            "property_instance": self.property_instance,
            "property_router": self.property_router,
            "ownership_instance": self.active_ownership
        }

    @snitch_func
    def parcel_is_transactable(self, validate=True):
        """Call this method. Raise error if anything happens"""
        self.validate = validate
        try:
            if self.validate:
                self._(self.check_inhibiting_ongoing_processes)

            if self.configs['property_in_registration']:
                self._(self.get_property_instance_instance_as_dict)

                if self.validate:
                    self._(self.validate_land_reg_property)

                    if self.nature_of_title == "LEASEHOLD" and not self.property_instance['county_parcel']:
                        self._(self.validate_land_admin_leaseholds)

            if self.validate:
                if self.configs['parcel_in_survey']:
                    self._(self.validate_survey_parcel_status)

            # process not allowed if invoices not settled
            if settings.SECRET_KEY != "secret" and validate:
                if self.configs['validate_invoices']:
                    self._(self.parcel_no_pending_invoices)
        except ValueError as e:
            return self.false_res(e)

        return self.true_res("Parcel can be used for transaction")

    def get_property_instance_instance_as_dict(self):
        success, info = registration_property_details(property_number=self.parcel_number,
                                                      headers=self.context['headers'])
        if not success:
            return self.false_res(info.get('details', info.get('detail')))
        else:
            self.property_reg_details = info['details']
            if self.validate:
                success, info = self._check_vals('Property', self.property_reg_details, [
                    {'property_status': ['ACTIVE', 'Property is not active']},
                    {'validation_status': ['VALIDATED', 'Property is not valid']},
                ])
                if not success:
                    return self.false_res(info)

            """change object of the received data to fit object"""
            success, info = self.recalibrate_property_instance_to_return_active_useful_entries()
            if not success:
                return self.false_res(info)
        return True, "Very fine"

    def get_transactable_register(self):
        allowed_nature_of_title_in_order_of_preference = ["LONG_TERM_LEASE", "SECTIONAL_PROPERTY", "LEASEHOLD",
                                                          "FREEHOLD"]

        """the lambda below returns the register with min index of nature of title as above. only active registers"""
        """soon, add a filter if term is past today since 'lease_from'"""
        try:
            self.property_router = min((entry for entry in self.property_reg_details.get('register', []) if
                                        (entry['property_status'] == "ACTIVE" or not self.validate)),
                                       key=lambda x: allowed_nature_of_title_in_order_of_preference.index(
                                           x['nature_of_title']))
        except:
            return self.false_res('This property has no transactable register.')
        """return void"""
        return self.true_res('Very fine')

    def recalibrate_property_instance_to_return_active_useful_entries(self):
        self.property_instance = self.property_reg_details
        if bool(self.property_reg_details.get('register', [])):

            """choose the first of register if nature of title provided or in the required order"""
            success, info = self.get_transactable_register()
            if not success:
                return self.false_res(info)
            self.nature_of_title = self.property_router['nature_of_title']
            self.readable_nature_of_title = self._r(self.property_router['nature_of_title'])

            if self.nature_of_title == "LONG_TERM_LEASE":
                self.configs['parcel_in_survey'] = False

        """set property instance dict"""
        self.property_instance = self.property_reg_details
        if self.property_instance:
            try:
                self.active_ownership = \
                [ownership for ownership in self.property_router['ownership'] if ownership['active']][0]
            except:
                pass

        return True, 'Done'

    def validate_land_reg_property(self):
        """ENUMERATION STATUS"""
        if self.property_instance['enumeration_status'] != self.configs['enumeration_status'] and self.configs[
            'enumeration_status'] != "ALLOW_ANY":
            return self.false_res(
                f"{self.parcel_number} ({self.readable_nature_of_title}) enumeration status is not valid for this transaction.")

        """PROPERTY STATUS OF PROPERTY INSTANCE"""
        if self.property_instance['property_status'] != self.configs['property_status']:
            return self.false_res(
                f"Parcel number {self.parcel_number} ({self.readable_nature_of_title}) is {self.property_instance['property_status']}.")

        """VALIDATION STATUS - the  nature of data posted, if no errors"""
        if self.property_instance['validation_status'] != self.configs['validation_status']:
            return self.false_res(
                f"Parcel number {self.parcel_number} ({self.readable_nature_of_title}) is {self.property_instance['validation_status']}")

        """Property register"""
        if self.configs['property_has_register']:
            """Property must have an active register"""
            if not self.property_router:
                return self.false_res(
                    f"Property number {self.parcel_number} ({self.readable_nature_of_title}) does not have any register")

            """Check nature of title"""
            if self.configs['register_nature_of_title'] != "ALLOW_ANY":
                if self.property_router['nature_of_title'] != self.configs['register_nature_of_title']:
                    return self.false_res(
                        f"A {self._r(self.configs['register_nature_of_title'])} register is required for this transaction.")

            """Inhibitions, court orders, caveats"""
            inhibitions = [prop for prop in self.property_router['proprietorship_section'] if
                           prop['inhibition'] in self.configs['inhibiting_inhibitions'] and prop['status'] in ["ACTIVE", None]]
            if bool(inhibitions):
                return self.false_res(
                    f"{self.parcel_number} ({self.readable_nature_of_title}) has an active {self._r(inhibitions[0]['inhibition'])} preventing this transaction")

            """Inhibitions, court orders, caveats"""
            if bool(self.configs['required_inhibitions']):
                inhibitions = [prop for prop in self.property_router['proprietorship_section'] if
                               prop['inhibition'] in self.configs['required_inhibitions'] and prop['status'] in ["ACTIVE", None]]
                if not bool(inhibitions):
                    return self.false_res(
                        f"{self.parcel_number} ({self.readable_nature_of_title}) should have an active {self._r(inhibitions[0]['inhibition'])} for this transaction")


            """Encumbrances, eg charge, long term lease"""
            if bool([prop for prop in self.property_router['encumbrance_section'] if
                     prop['nature_of_encumbrance'] in self.configs['inhibiting_encumbrances'] and prop['status'] in [
                         "ACTIVE", None]]):
                return self.false_res(
                    f"{self.parcel_number} ({self.readable_nature_of_title}) has an active encumbrance preventing this transaction")

            """required encumbrances"""
            if bool(self.configs['required_encumbrances']):
                if not bool([prop for prop in self.property_router['encumbrance_section'] if
                             prop['nature_of_encumbrance'] in self.configs['required_encumbrances'] and prop[
                                 'status'] in ["ACTIVE", None]]):
                    return self.false_res(
                        f"{self.parcel_number} ({self.readable_nature_of_title}) should have an active {self._r(self.configs['required_encumbrances'][0])} encumbrance")

            """Active ownership ? """
            active_ownership = [ownership for ownership in self.property_router['ownership'] if ownership['active']]
            if not bool(active_ownership):
                return self.false_res(
                    f"{self.parcel_number} ({self.readable_nature_of_title}) does not have an active ownership")
            if len(active_ownership) > 1:
                return self.false_res(
                    f"{self.parcel_number} ({self.readable_nature_of_title}) has conflicting ownership data.")
            self.active_ownership = active_ownership[0]
            if "ALLOW_ANY" not in self.configs['ownership_holding_type']:
                if self.active_ownership['holding_type'] not in self.configs['ownership_holding_type']:
                    return self.false_res(
                        f"Invalid ownership type for {self.parcel_number} ({self.readable_nature_of_title}) for this process.")

        """Return Gibberish"""
        return True, "Fine"

    def validate_survey_parcel_status(self):
        """Survey data to be valdiated from survey department"""
        survey_query = [
            {'exists': [self.configs['parcel_in_survey'], f' Survey parcel status for {self.parcel_number} is invalid.']},
            {'property_status': [self.configs['survey_status'], f'Survey parcel {self.parcel_number} is not active']},
            {'validation_status': [self.configs['survey_validation_status'], f'Survey parcel data for {self.parcel_number} is not valid']}
        ]
        survey_details_ = survey_details(
            parcel_number=self.parcel_number,
            headers=self.context['headers']
        )
        survey_query += [
            {key: [val, f'Survey Status error for {self._r(key)}']} for key, val in self.configs['survey_parcel_props'].items()
        ]

        return self._check_vals(
            name='Survey parcel',
            obj=survey_details_,
            query=survey_query
        )

    def validate_land_admin_leaseholds(self):
        """Validate for leasehold parcels that are to be transacted"""
        land_admin_query = [
            {'exists': [True, f'Property lease for {self.parcel_number} does not exist.']},
            {'valid': [True, f'Property lease for {self.parcel_number} is not valid.']},
            {'active': [True, f'Property lease for {self.parcel_number}is not active.']}
        ]
        land_admin_details = get_land_admin_ingestion_parcels(parcel_number=self.parcel_number, headers=self.context['headers'])
        return self._check_vals(
            name='Property Lease',
            obj=land_admin_details,
            query=land_admin_query
        )

    def parcel_no_pending_invoices(self):
        parcel_pending_invoices = get_parcel_invoices_status(
            parcel_number=self.parcel_number,
            multiple_status=['PENDING', 'PARTIAL'],
            page_size=100,
            headers=self.context['headers']
        )
        if parcel_pending_invoices:
            non_search_invoices = [invoice for invoice in parcel_pending_invoices['results'] if invoice['fee_schedule'] != "DLR_0040_1000"]
            if bool(non_search_invoices):
                return self.false_res(f'Parcel has {len(non_search_invoices)} pending system invoices. Cannot proceed.')
        return True, "Done"

    def check_inhibiting_ongoing_processes(self):
        # if settings.SECRET_KEY != "secret":
        #     current_processes = RegistrationServicesLinkages.objects.filter(
        #         Q(parcel_number=self.parcel_number) |
        #         Q(linkage_parcel_numbers__parcel_number=self.parcel_number),
        #         application_status='ONGOING'
        #     ).exclude(process_name__in=self.configs['allowed_ongoing_processes'])
        #     if current_processes.exists():
        #         processes = list(current_processes.all().values_list('process_name', flat=True))
        #         return self.false_res(f"There are ongoing process for this parcel: {self._r(list(set(processes[0:2])))}. Please await their completion.")
        return True, "Fine"


def _f(s) -> str:
    return s.replace(' ', '').capitalize()
