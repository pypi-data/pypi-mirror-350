
DEFAULT: dict = {
    # registration service statuses
    "property_in_registration": True,
    # general property status - it is not closed or destroyed
    "property_status": "ACTIVE",
    # enumeration status. some can be enumerated. if any, 'ALLOW_ANY'
    "enumeration_status": "ENUMERATED",
    # parcel must always be validated - data is safe and no errors found
    "validation_status": "VALIDATED",
    # reg processes should have registers. Except long term leases, or lease processes
    "property_has_register": True,
    # nature of title: eg long term transfer should have 'LONG_TERM_LEASE' only
    "register_nature_of_title": "ALLOW_ANY",
    # should register be active? Must be closed for lease process for instance, if any;
    "register_status": "ACTIVE",
    # ownership? if for transfer, can only allow specific ownership formats
    "ownership_holding_type": ["ALLOW_ANY"],
    # for instance, lra39 will only allow ADMINISTRATOR to transact
    "ownership_proprietor_rights": "PROPRIETOR",
    # encumbrances. some are inhibiting. pass [] if can transact when encumbrered, eg further charge
    "inhibiting_encumbrances": ["CHARGE", "LONG_TERM_LEASE", "FURTHER_CHARGE", "REPLACEMENT_CHARGE"],
    # these are proprietorship sections, such as court orders, and restrictions;
    "inhibiting_inhibitions": ["CAUTION", "INHIBITION_ORDER", "INHIBITION-ORDER", "RESTRICTION", "CAVEAT"],
    # some processes require encumbrances, eg discharge of charge, or LRA 61
    "required_encumbrances": [],
    # some processes will require caveats, or cautions to be removed
    "required_inhibitions": [],
    # the listed processes are allowed for virtually any process: they should not prevent other processes from happening
    # caution and court orders are allowed, since they may be maliciously applied by other parties to prevent transactions
    "allowed_ongoing_processes": ["ENUMERATION", "INHIBITION-ORDER", "SEARCH", "RESTRICTION", "CAUTION",
                                  "PRINT TITLE LEASE CERTIFICATE", "COURT-ORDER", "POWER-OF-ATTORNEY",
                                  "PRINT IR TITLE LEASE CERTIFICATE", "LRA_66_INHIBITION_ORDER", "STAMP-DUTY"],
    # survey processes validation
    "parcel_in_survey": True,
    "survey_status": "ACTIVE",
    "survey_validation_status": "VALIDATED",
    # by default, checks parcel invoices, all invoices must be paid for, except Search invoices
    "validate_invoices": True,
    # here, update any survey props. example: fixing requires 'boundary_type':'general' as a prop
    "survey_parcel_props": {}
}

