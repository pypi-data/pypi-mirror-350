# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
## [12.0.2.7.0] - 2024-07-29
### Added
- [#1262](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1262) Add mail activity team
- [#1144](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1144) Allow change mobile tariff wizard to join full sharing data bonds, in exchange of one sharing data mobile, which will quit the bond.

### Fixed
- [#1227](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1227) Move will_force_other_mobiles_to_quit_pack to mobile tariff wizard

## [12.0.2.6.4] - 2024-07-09
### Changed
- [#1243](https://git.coopdevs.org/coopdevs/som-connexio/odoo/odoo-somconnexio/-/merge_requests/1245) Change xoln project selector as model 

## [12.0.2.6.3] - 2024-07-03
### Fixed
- [#1243](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1243) Add contract_ids to SwitchboardServiceContractInfo

## [12.0.2.6.2] - 2024-07-01
### Added
- [#1235](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1235) Add switchboard in cron_compute_current_tariff_contract_line
- [#1234](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1234) Add switchboard contract type to subscription OC
- [#1226](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1226) add param phone to crm_lead_service

### Changed
- [#1087](https://git.coopdevs.org/coopdevs/som-connexio/odoo/odoo-somconnexio/-/merge_requests/1087) Check sponsored code case insensitive

## [12.0.2.6.1] - 2024-06-18
### Added
- [#1217](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1217) Added vodafone coverage to contract change adress
- [#1194](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1194) Added new warning confirmation message to change tariff wizzard and added condition to terminate contract warning message
- [#1180](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1180) Add data business analytics menu entry

### Fixed
- [#1174](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1174) Correos SIM devolution process

### Changed
- [#1109](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1109) Allow to change packs altogether with change holder wizard

## [12.0.2.6.0] - 2024-06-05
### Added
- [#1205](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1205) Add EiE products

### Changed
- [#1218](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1218) Add new discovery channels

## [12.0.2.5.11] - 2024-05-14
### Added
- [#1197](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/nn) Add source param to create subscription request
- [#1189](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1189) Added is_in_CM_program to marginalized group domain
- [#1145](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1145) Add new feature to search contracts by customer ref filtering with phone number and subscription technology

## [12.0.2.5.10] - 2024-03-15
### Added
- [#1191](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1191) Add fiber communitary products and Can Carné project
- [#1168](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1168) created new group in data and added condition to can create activity type"
- [#1147](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1147) Check mobile consumption with a mobile contract wizard

### Changed
- [#1188](https://git.coopdevs.org/coopdevs/som-connexio/odoo/odoo-somconnexio/-/merge_requests/1188) change value to Min attribute TConserva in product_attribute_value.xml
- [#1182](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1182) Made parent pack contract id visible in mobile contract view
- [#1177](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1177) Changed to explicit translations
- [#1153](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1153) Send CRM Lead phone as contact phone to OTRS tickets

## [12.0.2.5.9] - 2024-03-04
### Added
- [#1075](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1075) Add minutes and data attributes for mobile contracts in get contract API.

### Fixed
- [#1189](https://git.coopdevs.org/coopdevs/som-connexio/odoo/odoo-somconnexio/-/merge_requests/1183) Fix available_operations in adsl without fix

## [12.0.2.5.8] - 2024-02-12
### Added
- [#1173](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1173) Add `code` to previous provider tree view
- [#1167](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1167) Created computed field to check if CRM Lead lines has any BA with applied location change, then hidden the button Add Line in the CRM Lead

### Fixed
- [#1179](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1179): Fix default IBAN with contract address change: take the one from the current mandate id instead of the first from the partner's list.

## [12.0.2.5.7] - 2024-01-26
### Added
- [#1159](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1159) Added new terminate contract reason and popup alert

## [12.0.2.5.6] - 2024-01-26
### Changed
- [#1172](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/1172) Upgrade OTRS-SC version to 1.5.2 to fix SetSIMRecievedMobileTicket misfunctioning.

## [12.0.2.5.5] - 2024-01-23
### Changed
- [#1170](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/1170) Upgrade OTRS-SC version to 1.5.1 to adapt OTRS migration to version 8.

## [12.0.2.5.4] - 2023-12-27
### Added
- [#861](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/861) Set a cron to activate change tariff tickets from OTRS programatically

### Changed
- [#1162](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1162) Changed field name when asociatel is the supplier

## [12.0.2.5.3] - 2023-12-20
### Added
- [#1157](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1157) Add marginalized collective logic

### Fixed
- [#1158](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1158) View vodafone_id with form contract view for asociatel
- [#1155](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1155) Use showed_name instead of custom_name for product description in our contract service API.

### Changed
- [#1152](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1151): Changed activity type portability names

## [12.0.2.5.2] - 2023-11-20
### Added
- [#1142](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1142): With Coop Agreements, show their related partner's name instead of their code.
- [#1143](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1143) Create BankUtils service
- [#1131](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1131) Add Asociatel fiber supplier

### Fixed
- [#1139](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1139) Retry TimeOut error on track correos delivery job
- [#1141](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1141) Fix disable login controller. Allow to login using the SSO.

## [12.0.2.5.1] - 2023-11-02
### Added
- [#1032](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1032) Disable Odoo login.

### Fixed
- [#1137](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1137) Fix first_day_next_month problem with december month

## [12.0.2.5.0] - 2023-10-27
### Added
- [#1112](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1112) Add contract groups management.
- [#1118](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1118) Add TrucadesIllimitades12GB product
- [#1126](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1126) Order activity tree view by by deadline
- [#1130](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1130) Add partner bank id to default get of contract address change wizard
- [#1132](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1132) Add fibracat as previous provider
- [#1134](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1134) Add code field in contract terminate reason and contract terminate user reason data.
- [#1135](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1135) Add an API endpoint to terminate contracts

### Fixed
- [#1106](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1106) Always set date_end to lastest line when executing the change tariff wizard

### Changed
- [#1128](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1128) Move IBAN from CRMLead to CRMLeadLine
- [#1129](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1129) Deleted on change logic to keep activity fields
- [#1133](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1133) Changed field in the view

## [12.0.2.4.0] - 2023-10-09
### Added
- [#1102](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1102) Add button to send new email for manually created leads
- [#1103](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1103) Add button to add new mobile crm lead to any lead
- [#1104](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1104) Track relabeled deliveries from correos
- [#1108](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1108) Add new coop agreeement endpoint

### Changed
- [#1036](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1036 ) Change the dates activation and introduced to send to OTRS.
- [#1100](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1100) Refactor to adapt to the new SetSIMRecievedMobileTicket API

## [12.0.2.3.8] - 2023-09-20
### Fixed
- [#1095](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1095) Fix filter out pack ok products in create lead from partner wizard
- [#1101](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1101) Example text

### Changed
- [#1097](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1097) Add new activity types

## [12.0.2.3.7] - 2023-09-13
### Fixed
- [#1016](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1016) Limit track_correos_delivery job to one channel

## [12.0.2.3.6] - 2023-08-21
### Added
- [#1079](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1079) Add API to expose one shots
- [#1089](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1089) retry job track correos delivery in crm lead

### Fixed
- [#1071](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1071) Fix fibers available to link: add shared bond change tariff tickets
- [#1091](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1091) When a new contract joins two sharing contracts by their shared bond id, only change their tariffs if needed

## [12.0.2.3.5] - 2023-08-17
### Added
- [#1072](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1072) When a mobile contract changes its tariff or is being terminated, in case it used to share data with others, we need to manage their tariffs accordingly.
- [#1082](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1082) When a new contract joins a shared bond, change tariffs according to the number of contracts sharing.
- [#1083](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1083) Add parent_pack_contract_id in contract view, only visible and editable for IT group
- [#1088](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1088) Fer saltar un error en cancel·lar una petició de sòcia amb factures encara obertes

## [12.0.2.3.4] - 2023-08-02
### Added
- [#1078](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1078) Add Virgin Telco previous provider
- [#1077](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1077) Add wizard to add mobile lines to an existing fiber CRMLead.
- [#1074](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1074) Add existing shared bond option to change mobile tariff wizard.

### Changed
- [#1073](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1073) Allow to duplicate Coop Agreement instances keeping the unique code constraint by adding a new default code when copying the model

## [12.0.2.3.3] - 2023-06-30
### Fixed
- [#1066](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1066) Ensure 'fiber_linked' is sent with the code from the selected fiber contract (if sharing data product)
- [#1067](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1067)
- [#1068](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1068) Add shared bond manage to change tariff api process

## [12.0.2.3.2] - 2023-06-19
### Fixed
- [#1065](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1065): Remove "shared_bond_id" type restriction from cerverus schema

## [12.0.2.3.1] - 2023-06-19
### Fixed
- [#1062](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1062) Sharing data products cannot be returned from product's `get_offer` or `get_product_wo_offer` methods

## [12.0.2.3.0] - 2023-06-19
### Added
- [#1048](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1048) Add product ba mm attribut to fiber data
- [#1052](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1052) Improve contract API:
    - Add pagination
    - Add more contract info in the response
    - Add shared data info
- [#1053](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1053) Add fiber 300 pack with IL 20 mobile as product and product_pack_line
- [#1060](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1060) Fix: do not apply offer-no-offer logic to sharing data mobile products

### Fixed
- [#1040](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1040) Do not relete mobiles with new location change fiber contracts

### Changed
- [#1045](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1045) feat(ContractMobileTariffChangeWizard): Add new shared bond option

## [12.0.2.2.2] - 2023-06-12
### Added
- [#1044](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1044) Allow to get fibers packed when wanting to add mobiles sharing data with `mobiles_sharing_data` parameter flag in api call.
### Removed
- [#1049](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1049) Revert (https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/908)

## [12.0.2.2.1] - 2023-06-05
### Added
- [#1042](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1042) Show sharing data contracts in related contracts smart button

## [12.0.2.2.0] - 2023-05-23
### Added
- [#849](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/849) Add 'has_landline_phone' attribute in product catalog and filter out products with internal flag 'contract_as_new_service' set to False
- [#1018](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1018) Add shared bonds mobile products
- [#1022](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1022) Add share_bond_id to link sharing data mobile contracts
- [#1025](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1025) Add shared bonds mobile products
- [#1038](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1038) Add fields to pack/shared_bounds
- [#1039](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1039) Add shared bond product packs and pack lines

### Fixed
- [#1030](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1030) Fix contract filters.
- [#1031](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1031) Fix ContractLines view inside the Contract view.
t validation
- [#1033](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1033) Fix process to sponsor an old member.
- [#1034](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1034) Change Contract Address Change product domain to fix the available products in this proces.
- [#1037](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1037) Fix archive partner and contract

### Changed
- [#908](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/908) Add pagination to Contract API
- [#998](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/998) Example text
- [#1025](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1025) Remove public condition in mobile_tariff_change_wizard
- [#1035](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1035) Use somconnexio as default previous provider in Change contract address wizard

## [12.0.2.1.14] - 2023-04-20
### Changed
- [#213](https://git.coopdevs.org/coopdevs/som-connexio/otrs-somconnexio/-/merge_requests/213) Upgrade dependency otrs-somconnexio to version 0.4.46

## [12.0.2.1.13] - 2023-04-19
### Added
- [#1027](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1027) Install auth_oidc to configure SSO.

## [12.0.2.1.12] - 2023-04-04
### Changed
- [#986](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/986) Complete workflow for Correus sim delivery monitoring

## [12.0.2.1.11] - 2023-04-04
### Added
- [#1014](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1014) Filter broadband contracts also by router 4G ICC
- [#1015](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1015) Add partner tags related field
- [#1017](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1017) Set max retries to 3 in track correos delivery job

### Fixed
- [#1016](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1016) Use has_active_contract field in running contract filter

### Changed
- [#1012](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1012) Remove groups attribute in `is_company` SR field, to allow this field to be seen by all users
- [#1013](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1013) Use change tariff wizard when breaking pack

## [12.0.2.1.10] - 2023-03-20
### Added
- [#990](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/990) Link new fiber contract with existing mobile contracts

## [12.0.2.1.9] - 2023-03-15
### Fixed
- [#1009](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1009) Fix Correos Seguimiento usage with the changes in the API.

## [12.0.2.1.8] - 2023-03-13
### Changed
- [#979](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/979) Allow to create contracts without "vodafone_contract_code"
- [#970](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/970) Mail Activity Type diversification

### Fixed
- [#996](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/996) feat: add 02 as previous provider
- [#991](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/991) Fix change holder wizard. Pack fiber only if new mobile contract product is pack exclusive.
- [#977](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/977) Fix Address Change process in contracts in pack
- [#886](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/886) Normalize the uses of VAT

## [12.0.2.1.7] - 2023-03-01
### Changed
- [#973](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/973) Update sim sending letter template with correos SIM delivery

### Fixed
- [#989](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/989) Fix condition to link OTRS tickets
- [#993](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/993) Do not break pack contract with fiber tariff change
- [#1004](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1004) Fix translations of menu entries.

### Removed
- [#995](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/995) Delete CRMLeadLine "activation_notes"

## [12.0.2.1.6] - 2023-02-27
### Fixed
- [#1000](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1000) Send subdivision code to OTRS without the country code.
- [#994](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/994) Fix contract holder change available products: filter by old product category

### Changed
- [#997](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/997) When changing a contract's holder, the new contract should start one day after the end date from the old one.

## [12.0.2.1.5] - 2023-02-23
### Changed
- [#872](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/872) Substitute sponsor_id by sponsor_ref in partner API result

### Fixed
- [#1003](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/1003) Remove the ICC field in the contract search view

## [12.0.2.1.4] - 2023-02-22
### Added
- [#981](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/981) Add Router 4G ICC parameter
- [#992](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/992) Add three HRAttendancePlaces

### Fixed
- [#988](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/988) Add active employees domain to HR reports.

### Changed
- [#984](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/984) Change mail_mail_statitcs tree view

## [12.0.2.1.3] - 2023-02-08
### Added
- [#982](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/982) Set fiber_contract_code to pack mobile ticket within lead provisioning
### Fixed
- [#983](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/983) Use sudo() with change tariff run_from_api method

## [12.0.2.1.2] - 2023-02-02
### Fixed
- [#978](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/978) Fix BadRequest error with parent_pack_contract_id

## [12.0.2.1.1] - 2023-02-01
### Added
- [#955](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/955) Cron correos api seguimiento
- [#972](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/972): Add `has_grouped_mobile_with_previous_owner` field to FiberDataFromCRMLeadLine

### Fixed
- [#971](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/971) Add combination for Vodafone,4G and Additional Service (fixed IP)
- [#975](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/975) Filter only mobile active lines for sims_to_deliver

## [12.0.2.1.0] - 2023-01-30
### Added
- [#950](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/950) Add Correos integration to deliver the SIM letter.

### Fixed
- [#958](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/958) Allow 'contract_line' with mobile '_is_pack' method

## [12.0.2.0.1] - 2023-01-26
### Fixed
- [#967](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/967) Fix 'fiber_linked' parameter assignation in ContractMobileTariffChangeWizard

## [12.0.2.0.0] - 2023-01-23
### Added
- [#896](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/896): Feature PACKS. Add new mobile product associated with fiber contract

Including all changes below:

### Added
- [#867](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/867) Expose packs in catalog pricelist
- [#897](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/897) Unblock mobile ticket in ba contract creation
- [#898](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/898) Link PACK OTRS tickets after their creation during pack provisioning
- [#890](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/890) Crm lead pack views
- [#891](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/891) Validations for Crm Lead from pack products
- [#902](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/902) Show pack contracts in smart button in Contract form
- [#909](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/909) Add fiber-contracts-to-pack API endpoint
- [#910](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/910) Check if product is in pack to relate the fiber contracts
- [#914](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/914) Allow to print SIM letter for each mobile lead line within lead
- [#920](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/920) Add OdooContractRefRelacionat to Change Tariff api
- [#921](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/921) Add has_vinculated_contracts to tree view
- [#922](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/922)  Add search filters for CRM lead packs according to their lead line content, and update their available actions
- [#924](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/924) Break packs if the ba contract ends
- [#928](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/928) Add introduced date to UnblockMobilePackTicket
- [#929](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/929) Add new pack-related parameters to customer and service data
- [#935](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/935) Allow filtering CRMLeads by their lead lines phone numbers
- [#939](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/939): Add wizard to change mobile tariffs by creating OTRS ChangeTariff Tickets.
- [#943](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/943) Exclude from method `get_fiber_contracts_to_pack` fiber contracts already referenced within mobile change tariffs or within new  mobile provisioning leads
- [#948](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/948) Add bonified mobile product logic with create lead from partner wizard
- [#951](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/951) Allow to link a mobile contract to a fiber one when OTRS already knows its reference (`parent_pack_contract_id`)

### Fixed
- [#903](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/903) Fix OTRSClient instanciation with 'link_pack_tickets' job
- [#904](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/904) Fix contracts pack relation by API with sudo in model searching
- [#907](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/907/) Remove pack validations
- [#915](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/915) Fix permissions error when creating mobile contract from OTRS
- [#916](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/916) Make all mobile lead lines from pack CRMLead be sent to OTRS as pack
- [#917](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/917) Fix error with crm pack activation notes
- [#923](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/923) Fix mobile lead line ids view in crm
- [#928](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/928) Fix CRMLeadRemesaWizard action_set_remesa object reference
- [#930](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/930) Fix typo parentheses order with translate function
- [#937](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/937) OdooContractRefRelacionat -> parent_pack_contract_id in Contract Change Tariff
- [#946](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/946) Serialize effective_date to string to create a OTRS ticket
- [#947](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/947): Break pack if new mobile product is not bonified with contract tariff change wizard.
- [#949](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/949) Fix(ContractMobileTariffChangeWizard): partner attribute with language assignation
- [#952](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/952) Exclude terminated contracts from `get_fiber_contracts_to_pack` result
- [#953](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/953) With contract holder change wizard check available fibers from new contract partner, not old one
- [#954](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/954) Use available_products instead of product_domain with Contract Change Tariff Wizard
- [#956](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/956) Use default_code instead of code to search the products to add IsInPack attribute
- [#957](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/957) Fix mobile tariff change wizard: always pass send_notification parameter
- [#963](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/963) Fix the DF sent to OTRS in change of tariff when break a pack contract.
- [#965](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/965) Fix test-create-fiber-unblock-mobile-ticket-with-holiday
- [#964](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/964) Fix BadRequest error with parent_pack_contract_id

### Changed
- [#870](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/870) Change crm.lead.line creation template to crm.lead
- [#893](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/nn) New packs without pack_type attribute
- [#900](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/900) Link pack contracts after creation.
- [#905](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/905) Add offer attribute to catalog products
- [#912](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/912) Update CRM Lead Pack views
- [#913](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/913) Hide publish button if product is pack exclusive
- [#919](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/919) Raise error if parent pack contract does not exist
- [#925](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/nn) Add validation for ICC in crm.lead when are set won
- [#926](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/926) Adapt Change address process to packs.
- [#927](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/927) Update crm lead creation mail
- [#933](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/933) Archive and restore crm_lead_line from form view
- [#934](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/934) Move to new CRMLead pack form view after CreateLeadFromPartnerWizard usage
- [#938](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/938) Removed unused columns in related contract tree view
- [#944](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/944) Adapt Change holder wizard to packs flow
- [#960](https://git.coopdevs.org/coopdevs/som-connexio/odoo-somconnexio/-/merge_requests/960) When creating a fiber contract associated with mobile, send both activation and introduced dates to UnblockMobilePackTicket service in OTRS


## [12.0.1.10.0] - 2023-01-17
### Added
- [#942](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/942) Add account asset report

### Changed
- [#739](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/739) Update aeat modules

## [12.0.1.9.14] - 2022-12-13
### Added
- [#888](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/888) Add previous service crm lead creation wizard

## [12.0.1.9.13] - 2022-10-17
### Added
- [#888](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/888) Add 4G category products in API product catalog
- [#878](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/878) Add router model ADOC R45 for router4G contracts

### Changed
- [#899](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/899) Make admin default user_id for mail_activity

## [12.0.1.9.12] - 2022-10-11
### Added
- [#886](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/886) Add has_active_contracts parameter to partner_otrs_view.py

## [12.0.1.9.11] - 2022-09-15
### Fixed
- [#884](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/884) Fix general.ledger.report when filtering by company

## [12.0.1.9.10] - 2022-09-14
### Added
- [#880](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/880) Add filter for Orange BA contracts
- [#879](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/879) Add field current_tariff_start_date in contract
- [#875](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/875) Audit sponsor_id, is_sponsee, coop_agreement and coop_agreement_id
- [#874](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/874) Add option to filter by 'general expenses' in General Ledger Report
- [#866](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/866) Add orange provider translations
- [#863](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/863) Creation of new pack products
- [#746](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/746) Checks for lang and indispensable emails
- [#699](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/699) Add wizard to confirm payments on invoicing tree view

### Fixed
- [#877](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/877) Rename crm_lead_line `category_id` for `partner_category_id`
- [#820](https://trello.com/c/rBZH8SRo/1272-error-assumpte-mass-mailing) Untranslate mass_mailing subject
- [#747](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/747) Fixed translations in mail.compose.message

## [12.0.1.9.9] - 2022-09-01
### Added
- [#723](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/723) Install l10n_es_toponyms.

### Changed
- [#864](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/864) Update Order Id translations

## [12.0.1.9.8] - 2022-08-17
### Added
- [#844](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/844) Add inactive_sponsored field to get Partner API response

### Changed
- [#867](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/867) Change parameter search incompatibility with product_catalog API
- [#862](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/862) Available products now uses root category
- [#858](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/858) Do not update mailing templates with each deploy
- [#857](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/857) Update the sim_sending_letter_template

### Fixed
- [#850](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/850) Restore previous-service in crm_lead api
- [#809](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/809) Fix concurrency error when validating sub req from wizard

## [12.0.1.9.7] - 2022-07-20
### Changed
- [#825](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/825) Use partner to render mass_mailing test
- [#750](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/750) Unsubscribe link now sets a flag in partner

## [12.0.1.9.6] - 2022-07-13
### Added
- [#853](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/853) Add address fields to client contracts view
- [#852](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/852) Add erpeek script to update contract line products from csv data

## [12.0.1.9.5] - 2022-07-06
### Added
- [#845](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/845) Add chatter to `product.product` model
- [#783](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/783) Add a list of products available for change tariff in Product catalog

### Fixed
- [#846](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/846) Do not check phone's duplicity with location change crm lines

### Changed
- [#848](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/848) Remove default start date from change tariff wizard

## [12.0.1.9.4] - 2022-06-21
### Added
- [#841](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/841) Add address,city to broadband contracts tree view
- [#833](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/833) Add reopen button to cancelled SR
- [#823](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/823) Send consideration notes to fiber and mobile OTRS tickets
- [#818](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/818) Create new '/api/partner/sponsees' endpoint to get sponsees information from a given partner
- [#780](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/780) Add chatter to AccountMove.

### Fixed
- [#840](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/840) Fix activity_type for One Shot w/o Cost
- [#839](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/839) Fix empty broadband isp info with change address wizard

### Changed
- [#838](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/838) Allow changing to SC cooperator agreement in partner view

## [12.0.1.9.3] - 2022-06-10
### Added
- [#807](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/807) Add partner action tags to allow to ban them to certain partners
- [#787](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/787) Set purpose in account payment order lines from Consumption Invoices
- [#732](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/732) Validate bank validation in partner creation and notify OTRS if from an API change IBAN request the corresponding bank does not exist in ODOO's database.

### Changed
- [#835](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/835) Remove force base_rest version to allow patched one

## [12.0.1.9.2] - 2022-06-01
### Added
- [#821](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/821) Set sponsorship hash to upper

### Fixed
- [#829](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/829) Fix syntax error that caused a warning with po files
- [#827](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/827) Do not store partner's has_lead_in_provisioning
- [#824](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/824) Filter out change holder/address CRM Leads when sending background emails

### Changed
- [#822](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/822) Upgrade base_rest

## [12.0.1.9.1] - 2022-05-26
### Fix
- [#828](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/828) Fix SR created as sponsorship and coop_agreement altogether

## [12.0.1.9.0] - 2022-05-25
### Added
- [#667](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/667) Add contract create reason

### Changed
- [#819](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/819) Extend update current contract line cron job to BA contracts
- [#816](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/816) Fix broadband_isp_info from portability lead lines without previous phone numbers and mark them with a boolean flag.

### Fixed
- [#720](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/720) Query to uniform missing phone_number to '-'
- [#719](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/719) Update logic criteria about products without fix, as well as crm leads or contracts related to them.

## [12.0.1.8.14] - 2022-05-11
### Changed
- [#812](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/812) Change SR API to create sponsorship_coop_agreement SR
- [#733](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/733) Make field delivery address not obligatory when icc is provided in wizard create lead

## [12.0.1.8.13] - 2022-05-04
### Added
- [#774](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/774) Allow Oneshot Router Return in 4G Vodafone

### Fixed
- [#805](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/805) Add New and Remesa stages of CRMLead to in provision concept
- [#800](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/800) Do not to empty previous provider's name or to edit their parameters from the form view

## [12.0.1.8.12] - 2022-05-03
### Added
- [#797](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/797) Add open_tab and vat to subscription.request tree view
- [#806](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/806) Add inactive sponsored flag to ResPartner
- [#802](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/802) Add partner's tag in crm lead line views

### Changed
- [#794](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/794) Remove start_date in Contract Iban and Partner Email Change wizard
- [#811](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/811) Search sponsorship_hash case insensitive in check_sponsor endpoint

## [12.0.1.8.11] - 2022-04-29
### Added
- [#804](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/804) Add migration to compute sponsorship hash in existent coop candidates
- [#788](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/788) Expose contracts by API with new endpoint `/api/contracts`

### Changed
- [#796](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/796) Inactive sponsees don't count and are highlighted
- [#801](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/801) Draft subscription requests count for sponsor limit

### Fixed
- [#803](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/803) [#799](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/799) [#795](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/795) Add sponsorship_hash logic to coop_candidates

## [12.0.1.8.10] - 2022-04-13
### Fixed
- [#792](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/792) Skip duplicated phone validation if phone number to be checked
- [#776](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/776) Remove old code from 'discontinued' product attribute

## [12.0.1.8.9] - 2022-04-06
### Added
- [#786](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/786) Expose sponsorship code and sponsees limit
- [#781](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/781) Show vodafone_id in Vodafone and Router4G contract form view.

### Fixed
- [#776](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/776) Set activity done to True and activity_type to one_shot

## [12.0.1.8.8] - 2022-04-04
### Added
- [#785](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/785) Subscription request sponsees limit validation
- [#784](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/784) Add sponsees number limitation
- [#779](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/779) Add sponsorship code
- [#643](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/643) Partner Email Change Endpoint

### Changed
- [#782](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/782) Fix EasyMyCoop version to 12.0.3.0.2.99.dev2 to aboid breaking changes.
- [#693](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/693) Invoice Line price unit set to amount untaxed
- [#692](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/692) Accept json as body param in application/x-www-form-urlencoded

## [12.0.1.8.7] - 2022-03-16
### Added
- [#775](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/775) Add boolean flag to partners which blocks automatized OC contract creation
- [#770](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/770) REVISAR FIX flag in OTRS
- [#743](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/743) Make cancelled crm lead lines visible and searchable
- [#630](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/630) Enviament de correu a les persones apadrinades per socis que es donen de baixa.

### Fixed
- [#769](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/769) Validate VAT also in modifications.
- [#762](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/762) Fix product catalog visibility in wizards.

## [12.0.1.8.6] - 2022-03-09
### Added
- [#772](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/772) Add Change Tariff BA button
### Fixed
- [#771](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/771) Allow non-string values for 'start_date' as change tariff API parameter

## [12.0.1.8.5] - 2022-03-02
### Added
- [#763](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/763) Add wizard Contract IBAN Change Force
- [#696](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/696) Add addresses information to the Partner API response
- [#647](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/647) Add discovery_channel to Partner computed from SubscriptionRequest

### Fix
- [#764](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/764) Allow OTRS formatted dates with change tariff API
- [#759](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/759) Ensure partner's cooperator flag is set to True when validating a SR from them
- [#754](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/754) Fix `ordered_parts` and `share_product_id` values for manually created SR depending on their `type`.

## [12.0.1.8.4] - 2022-02-23
### Added
- [#757](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/757)  Add Orange filter in BA contracts tree view
- [#746](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/746) Allow Router 4G ticket creation

### Fixed
- [#759](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/759) Skip oneshot products and terminated lines
- [#755](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/755) Fix typo in date.range perms for group_user
- [#748](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/748) Set company name as first name and not lastname in OTRS tiquets
- [#738](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/738) Allow One Shot w/o cost products
- [#721](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/721) Create copy contract service info when holder change

### Changed
- [#753](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/753) Edit mm_fiber_coverage and orange_fiber_coverage visibility in change address wizard
- [#750](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/750) Adapt change tariff API's endpoint to work with both mobile and fiber contracts

## [12.0.1.8.3] - 2022-02-16
### Added
- [#724](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/724) Check for not archived journal in Invoice validation
- [#726](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/726) Add separated public menu entry for date ranges
- [#725](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/725) Add comments, notes to account_asset

### Fixed
- [#714](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/714) Invoice claim mails sent only to customer

## [12.0.1.8.2] - 2022-02-14
### Added
- [#727](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/727) Install module l10n_es_aeat_mod347 and add a button to calculate it in backgorund.

### Fixed
- [#745](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/745) Fix Partner name search to don't filter the providers.

## [12.0.1.8.1] - 2022-02-07
### Added
- [#740](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/740) Allow to choose the starting date in change tariffs api calls
- [#716](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/716) Add street fields to otrs mobile ticket
- [#736](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/736) Add active field to mail.activity

## [12.0.1.8.0] - 2022-02-01
### Added
- [#735](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/735) Add Partner lang to Contract model and show it in the Contracts tree view.

### Fixed
- [#734](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/734) Assign name to router4G new contract when changing holders

### Changed
- [#729](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/729) Remove cancel button from planned activities
- [#710](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/710) Disable tracking in cron_compute_current_tariff_contract_line
- [#684](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/684) Remove products with DadesAddicionals500MB_product_template from one shot wizard
- [#635](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/635) Set product data as noupdate="1"
- [#604](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/604) Make change tariff button available only for IT group

## [12.0.1.7.11] - 2022-01-26
### Fixed
- [#730](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/730) Update vodafone related fields in contract

## [12.0.1.7.10] - 2022-01-25
### Added
- [#717](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/717) Allow router 4G contract creation from API and from create lead from partner wizard

### Fixed
- [#722](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/722) Allow to edit custom_name from a product attribute value

## [12.0.1.7.9] - 2022-01-18
### Added
- [#715](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/715) Add orange_fiber_coverage in CU
- [#709](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/709) Add Orange Fiber Service Supplier

### Fixed
- [#711](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/711) Removed lang from context in product_catalog_service

### Changed
- [#698](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/698) Use the showed name to define the Product name.
- [#674](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/674) Move subscription request type and add onchange for it
- [#665](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/665) Order menuitems to pop up attendance view when entering odoo

## [12.0.1.7.8] - 2022-01-07
### Added
- [#640](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/640) Give create permission to KPI expression of mis budget items
- [#617](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/617) Add description, operationDate to compensation wizard

### Fixed
- [#708](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/708) Renamed res_partner_form view to avoid redefinition
- [#707](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/707) Change in mobile_isp_info_has_sim change sets mobile_isp_info.has_sim
- [#706](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/706) Fix typo in fiber signal identifiers and their correspondence

### Changed
- [#703](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/703) Give IT group delete permission of contract lines on contract view

## [12.0.1.7.7] - 2021-12-20
### Added
- [#700](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/700) Add `fiber signal type` field in fiber contracts

## [12.0.1.7.6] - 2021-12-17
### Added
- [#695](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/695) Show full address instead of just the street in CU `previous_contract_address` field
- [#691](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/691) Show ADSL order-id in contract view and update its translation
- [#690](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/690) Add field has active contract to partner
- [#689](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/689) Show sponsees tab in coop candidates

### Fixed
- [#701](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/701) Fix service_partner for contract holder change wizzard
- [#697](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/697) Fix an attendance test which makes pipelines fail
- [#688](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/688) Fix error when filtering contracts by storing their vodafone_id value.
- [#626](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/626) Overload Payment Order method to empty parter in case of transfer account
- [#550](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/550) Upgrade account_payment_order to 12.0.1.6.3

### Removed
- [#694](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/694) Remove initial tests users and their partners

## [12.0.1.7.5] - 2021-11-26
### Added
- [#686](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/686) Add flag partner has_sim in crm_lead_line when icc field is provided
- [#683](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/683) Add Router 4G product
- [#682](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/682) Add notes in attendance model
- [#675](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/675) Mark weekends and holidays with a different color in the calendar.
- [#641](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/641) Add new public API endpoint to call change tariff wizard to apply changes in existing mobile contracts
- [#638](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/638) Add new public API endpoint to call one shot wizard and add additional bonds to existing mobile contracts

### Fixed
- [#669](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/669) Add cron to recompute current contract lines every month
- [#664](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/664) Fix typo in Discovery Channel name

### Changed
- [#680](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/680) Allow coop candidates to sponsor

## [12.0.1.7.4] - 2021-11-18
### Fixed
- [#678](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/678) Fix name searching in `mobile_contract_search_view`

## [12.0.1.7.3] - 2021-11-12
### Added
- [#662](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/662) Add a disenrollment reason field to fulfill when finishing a cooperator's membership

### Changed
- [#661](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/661) Make delivery_address not required if icc
- [#668](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/668) IBAN not required in SR API if is sponsored
- [#671](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/671) Phone number not required in broadband portability
- [#672](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/672) Set previous_service default in BroadbandISPInfo portability

### Fixed
- [#670](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/670) Birthdate not required in SubscriptionRequest API if is an organization.

## [12.0.1.7.2] - 2021-10-27
### Added
- [#660](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/660) Allow users to auto-validate their holidays

## [12.0.1.7.1] - 2021-10-25

### Added
- [#656](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/656) Add service state to contract search view
- [#652](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/652) Add contract groupby fields
- [#645](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/645) Save previous service address to BA contracts to send it to OTRS Change Address tickets
- [#634](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/634) Endpoint for Contract IBAN Change Wizard
- [#631](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/631) Added wizard to publish product in order to have confirmation dialog

### Changed
- [#642](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/642) Make fields readonly on subscription request view

### Removed
- [#657](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/657) Hide `tariff_product` field in contract custom search
- [#648](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/648) Remove validation of previous_service in BroadbandISPInfo

## [12.0.1.7.0] - 2021-10-19
### Added
- [#637](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/637) Hr attendance place options
- [#509](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/509) Modules for employee attendance and leaves

### Fixed
- [#632](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/632) Fix hr attendances translation

## [12.0.1.6.2] - 2021-09-29
### Added
- [#628](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/628) Add costs analytic accounts
- [#580](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/580) Add copy account_id of AccountInvoice in duplication.

### Fixed
- [#610](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/610) Activity now assigned to current user

### Changed
- [#460](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/460) Refactor 'body=' patch in rest controller to hooks.py

## [12.0.1.6.1] - 2021-09-21
### Added
- [#624](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/624) Add contract emails field to mobile contract sql view

### Fixed
- [#622](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/622) Fix contract terminate user reason table reference
- [#621](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/621) Fix manual subscription request vat message error
- [#587](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/587) Check if partner has shares active before validate a SR related with it.
- [#544](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/544) Only allow to create new contract service infos in BA contracts, add a log when editing them, and compute contract when contract service info change.

### Changed
- [#627](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/627) Add public attribute in product
- [#625](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/625) Renamed Xarxa Greta Fiber from 1Gb to 600Mb
- [#620](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/620) Make field coop agreement visible for edit.
- [#609](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/609) Use attributes to get catalog properties

## [12.0.1.6.0] - 2021-09-14
### Added
- [#619](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/619) Save old contract PON and fiber speed in address change CRMLeads, to send them to OTRS.
- [#583](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/583) Validate phone number before remesa stage
- [#582](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/582) Filter products by partner condition (coop_agreement, coop_sponsee)
- [#596](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/596) Add missing notes field to mobile crm lead line creation

### Fixed
- [#615](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/615) Add private field to private products in the catalog.
- [#614](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/614) Check if all lines are ended before terminate contract
- [#586](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/586) Use 'noupdate' in the static XML data files.

## [12.0.1.5.2] - 2021-09-07
### Added
- [#603](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/603) Add new fiber 100Mb without landline product
- [#601](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/601) Create mobile contract otrs view

### Fixed
- [#599](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/599) Avoid dividing by zero
- [#590](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/590) Fix international minutes products: delete the erroneous 200 minutes product and add the missing 600 minutes one.

### Changed
- [#605](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/605) Move change address wizard button to contract view
- [#601](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/601) Limit `update_ticket_with_coverage_info` method to BA tickets
- [#594](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/594) Moved OC code to async (job) in partner address updadte

## [12.0.1.5.1] - 2021-08-23
### Added
- [#581](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/581) Add service street, zip code and city filters to BA contracts

### Fixed
- [#593](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/593) Fix direct bytes case when it can base64 decoded right

### Changed
- [#592](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/592) Aged Partner Balance: group by partner, add vat

## [12.0.1.5.0] - 2021-08-10
### Added
- [#572](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/572) Add warning if vat already exists in contacts
- [#571](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/571) Fix "active" contract filter used in wizards.
- [#568](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/568) Activate concurrency check. This check don't allow to save if the record has been changed after you start to edit.
- [#563](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/563) Install web_m2x_options module
- [#558](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/588) Add spanish translation to product names
- [#518](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/518) Add `product-catalog` endpoint to our API to check the product catalog with their prices, according to different taxes.

### Fixed
- [#589](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/589) Update codes of non spanish banks
- [#585](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/585) Fix direct file in args case in payment return email gateway
- [#584](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/584) Fix last_return_amount in return invoice templates
- [#579](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/579) Add no update to Payment Modes data
- [#576](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/576) Add service address translation in crm lead search view
- [#561](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/561) Add category for La Borda products

### Changed
- [#578](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/578) Move the quick invoice jobs to the root channel.
- [#564](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/564) Relax router mac address validations

## [12.0.1.4.1] - 2021-07-22
### Fixed
- [#575](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/575) Force attachment conversion to str it is bytes

## [12.0.1.4.0] - 2021-07-21
### Added
- [#560](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/560) Add frequent fields filters to BA Lead Lines
- [#558](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/558) Add user id and tags for special organizations on partner and contract
- [#528](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/528) Add previous provider id to contract
- [#541](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/541) Email gateway to payment return import
- [#570](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/570) Reactivate validate_partner_bank_id for some actions

### Changed
- [#569](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/569) Improve Invoice Claim 1 template and add capital return case

### Fixed
- [#553](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/553) Use last return amount in invoice_claim_1_template
- [#567](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/567) Unset payment_mode_id in Credit Note creation
- [#565](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/565) Add country to CRMAccountHierarchyFromPartner white list

## [12.0.1.3.6] - 2021-07-14
### Added
- [#552](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/552) Coop agreement set sql constraints unique code

### Changed
- [#547](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/547) Modify the representation of FieldMany2ManyTagsContractEmail.
- [#537](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/537) Create somoffice user only for cooperator or customer
- [#535](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/535) Remove unused fields from broadboand model

### Fixed
- [#557](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/557) Remove duplicated translation entry

## [12.0.1.3.5] - 2021-07-07
### Added
- [#522](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/522) Add XOLN supplier and its Service Info
### Changed
- [#551](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/551) Forbid creating partner's invoice address

## [12.0.1.3.4] - 2021-07-05
### Added
- [#516](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/516) Add OC update when changing partner main address
- [#497](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/497) Add option to enqueue marking as uploaded Account Payment Order
- [#545](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/545) Add range for due_date/date in Create Transactions from Move Lines
- [#543](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/543) Add API endpoint to count how many members and contracts we have.

### Changed
- [#546](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/546) Reorder contract terminate reasons and contract terminate user reasons

### Fixed
- [#519](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/519) Normalize all high priorities to default one

### Removed
- [#548](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/548) Remove location and notes field from email and iban change wizards

## [12.0.1.3.3] - 2021-06-21
### Added
- [#521](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/521) Add order_id field to BA contracts
- [#514](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/514) Wizard force integration with OC

### Fixed
- [#529](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/529) Change compute effective date method to get the date from the last paid share.

## [12.0.1.3.2] - 2021-06-15
### Added
- [#524](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/524) Confirmation wizard before crm lead validation

### Changed
- [#539](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/539) Make change email wizard form view cleaner
- [#536](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/536) Merge the change contact and change OV email processes.

### Fixed
- [#538](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/538) Avoid expected singleton error in `_search_or_create_email` with duplicated child emails

## [12.0.1.3.1] - 2021-06-14
### Added
- [#526](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/526) Change OV user email from Partner email change wizard.
- [#525](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/525) Update ChangePartnerEmails wizard to update the contact email

### Changed
- [#530](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/530) Overwrite translation for mail module "Discard" button in `mail_activity_view_form_popup` view

### Fixed
- [#533](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/533) Don't allow edit email in partner form

## [12.0.1.3.0] - 2021-06-07
### Added
- [#512](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/512) Add code field to PriceList
- [#424](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/424) Contract Compensation Wizard which creates an activity with the amount or a One Shot in OC

### Changed
- [#507](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/507) Account Payment Line Create wizard queued and splitted in groups
- [#493](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/493) Low priority for invoice creation and validation

### Removed
- [#508](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/508) Remove La Borda product attribute values

## [12.0.1.2.7] - 2021-05-31
### Fixed
- [#517](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/517) Fix bug in mobile contract search view which didn't allow to search by partner.
- [#510](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/510) Convert to a regular member a partner with cooperative agreement now unsets coop_agreement_id.
- [#505](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/505) Add terminate contract reasons

### Changed
- [#496](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/496) Filter by active contract not_terminated
- [#469](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/469) Looking for partners' submails too in contract search

## [12.0.1.2.6] - 2021-05-21
### Fixed
- [#513](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/513) Fix remesa crm lead lines adding validation error
- [#511](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/511) Payment return match button account.move.lines now uses 'like' for reference instead of '='
- [#506](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/506) Convert the service "previous_owner_vat_number" with an actual VAT format.
- [#501](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/501) Save VAT from partner with create SR from partner wizard
- [#478](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/478) Remove duplicated request in terminate contract process
- [#441](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/441) Fixed domain to include `general` type journals in account return import

## [12.0.1.2.5] - 2021-05-18
### Fixed
- [#502](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/502) Fix syntax error in product search

## [12.0.1.2.4] - 2021-05-17
### Added
- [#499](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/499) Translate the name of the Discovery Channels
- [#495](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/495) Add create user to crm lead line tree view
- [#483](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/483) Add wizard to get partner's email from their SomOffice user

### Fixed
- [#490](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/490) Fix product name_search to include previous domain
- [#498](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/498) Make button reactivate contract available only for IT group
- [#496](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/496) Filter by active contract not_terminated
- [#470](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/470) Limit payment.return.import match to selected journal

### Changed
- [#491](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/491) Show more info in CRMLead Remesa validations and chech phone number in active contracts only.

## [12.0.1.2.3] - 2021-05-10
### Changed
- [#487](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/487) Move view to recently created CRMLeadLine in `create_lead_from_partner` and `contract_address_change` wizards, instead of the parent CRMLead
- [#471](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/741) Move CRMLead ValidationError for mutliple CRMLeadLines associated into `action_set_won` method from CRMLead

### Fixed
- [#486](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/486) Fix activity type record

### Removed
- [#488](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/488) Remove option to cancel a contract termination (reactivation)
- [#475](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/475) Remove action to duplicate a CRMLeadLine from their form view.

## [12.0.1.2.2] - 2021-05-03
### Added
- [#477](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/477) Add process to update provisioning ticket with coverage info

## [12.0.1.2.1] - 2021-04-28
### Added
- [#476](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/476) Add location filter to activities board

### Changed
- [#474](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/474) Add partner filters and remove invoice_partner_id from contract holder change wizard
- [#452](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/452) Update OC with just the email or iban changed through wizards
- [#443](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/443) Refactor CRMAccountHierarchyFromContractService class and rename it to CRMAccountHierarchyFromContractCreateService

### Removed
- [#480](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/480) Remove the manual action to publish the package in PyPI

## [12.0.1.2.0] - 2021-04-26
### Added
- [#453](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/453) Migrate translations of external modules
- [#443](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/443) Raise error with CRMAccountHierarchy fallback strategy
- [#442](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/442) Add contract terminate reasons
- [#412](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/412) Improve validations of SR and CRMLead in validation process:
  - SR: Don't allow validating if the IBAN bank is archived or doesn't exist in Odoo.
  - CRMLead:
    - Add REMESA stage
    - Raise error if Partner is not set.
    - Raise error if the IBAN bank is archived or doesn't exist in Odoo.
    - Raise error if exists a CRMLead or Contract with the same phone number.
    - Add wizard to change stage to Remesa allowing to skip the duplicated phone validation.

- [#394](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/394) Create activities after wizard execution

### Fixed
- [#472](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/472) Improve the CI:
  - Verify the Codecov Bash upload script integrity.
  - Add job to check if coverage decrease from a minimun configured.

### Changed
- [#465](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/465) Add delivery address in mobile service contract info model, and use it the new sim sending letter instead of the partner's invoice one.
- [#450](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/450) Activity date_done now editable and changes traceable

## [12.0.1.1.22] - 2021-04-21
### Fixed
- [#464](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/464) Add previous owner info to ISPInfo in the change address wizard
- [#462](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/462) Set cooperator_end_date empty in Partner if is coop_candidate or member

### Changed
- [#451](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/451) Only allow to modify Contract mandate and emails in creation.

## [12.0.1.1.21] - 2021-04-14
### Fixed
- [#461](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/461) Fix contract holder change wizard to allow setting new contract's banking mandate

## [12.0.1.1.20] - 2021-04-13
### Fixed
- [#457](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/457) Avoid error if 'firstname', 'lastname' or 'is_company' fields are not found as parameters in SubscriptionRequest creation.
- [#455](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/455) Fix default type in partner creation as "representative".

## [12.0.1.1.19] - 2021-04-12
### Fixed
- [#431](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/432) Avoid sending empty strings in ccEmails to OpenCell

### Changed
- [#455](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/455) Update company address
- [#421](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/421) Modify the SubscriptionRequest form:
  - Hide Company Type and Company Register Number.
  - Hide name and fill it with Company Name or firstname concat with lastname.
  - Fill the field state with the info of the partner selected as Cooperator.
  - Modify partner_id domain to don't show members and addresses/emails.
- [#332](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/332) Raise exception in background invoice process job if name (OC number) is duplicated

### Removed
- [#439](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/439) Remove res_partner options "contact" and "private address" in selection field "type"

## [12.0.1.1.18] - 2021-04-07
### Fixed
- [#416](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/416) Fix management of contact phone and email fields in create lead from partner wizard
- [#429](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/429) Fix "ref" and "code" assignation condition if coming empty with partner and contract models creation respectively.
- [#445](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/445) Set CRMLead `email_from` by default with partner's email.

### Changed
- [#446](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/446) Update aeat modules

## [12.0.1.1.17] - 2021-03-25
### Changed
- [#437](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/437) Modify the domains of journal ID and move lines in return payment form.

## [12.0.1.1.16] - 2021-03-24

### Added
- [#426](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/426) Add create_user_id to activity form and tree view.
- [#427](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/427) Add account payment terms (split payment in 3, 4, 5, 6 months).

### Fixed
- [#410](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/410) Restrict payment_mode_id by invoice_type (inbound or outbound).
- [#418](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/418) Ask for landline number when requesting to keep it in BA portability with create lead from partner wizard.
- [#420](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/420) Remove children partners from crm.lead partner_id.
- [#425](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/425) Filter out terminated BA contracts in CU wizard.
- [#435](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/435) Download OCB from Coopdevs fork in CI execution to fix the version.

### Changed
- [#428](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/428) Send to OTRs provision tickets the email from the service CRMLead instead of the one assigned to its partner.

## [12.0.1.1.15] - 2021-03-15

### Added
- [#409](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/409) Use OC invoice number in payment communication

### Fixed
- [#400](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/400) If there is not delivery_address in ISP Info creation, invoice address or main address are used
- [#411](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/411) Correct code showed in SIM letter to the corresponding CRM Lead Line ID.
- [#418](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/418) Ask for landline number when requesting to keep it in BA portability with create lead from partner wizard

## [12.0.1.1.14] - 2021-03-10

### Fixed
- [#405](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/405) Avoid odoo user preferred language to overwrite the email one (depending on the corresponding partner or SR) when sending the the CRM Lead creation email by manual action.

### Changed
- [#417](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/417) Improve error messages in contract API for tech / supplier dependencies

## [12.0.1.1.13] - 2021-03-05

### Added
- [#406](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/406) Show activities related to invoices in smart button of Partner view
- [#402](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/402) Add mail activity type data and translations

### Fixed
- [#397](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/397) Fix OC integration errors managing the priority and ETA time of delayed jobs.
- [#414](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/414) Remove duplicated entry in catalan i18n file which caused an error when trying to import and overwrite translation files.
- [#413](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/413) Force "showed name" in product to be set and stored in DB.

### Changed
- [#407](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/407) Show draft invoices in the invoices view opened from Invoiced smart button.

## [12.0.1.1.12] - 2021-03-03

### Added
- [#395](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/395) Checks if there's already a contract with the same ticket number

### Fixed
- [#399](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/399) Shows an error if there is not any mandate in partner that matches with the acc number in contract creation

### Changed
- [#389](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/389) Contract creation API moved to Queue Job

### Removed
- [#401](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/401) Removed old unused delivery_address and service_address for ISP Info creation in tests

## [12.0.1.1.11] - 2021-03-02

### Changed
- [#360](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/360) Compute the cooperator end date with the Subscription Register

### Added
- [#370](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/370) Add wizard to manage the payment group importation from Tryton data.
- [#379](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/379) Add translations to block button appearing in SR tree view to non-admin users

### Fixed
- [#388](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/388) Empty emails notificacions' layout

## [12.0.1.1.10] - 2021-02-24

### Fixed
- [#381](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/381) Let "sponsee" attribute appear and be editable from partner view only when the given partner is neither candidate nor effective cooperator.
- [#392](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/392) Make product_id editable on crm lead line mobile and BA views

## [12.0.1.1.9] - 2021-02-22

### Fixed
- [#384](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/384) Allow searching by DNI formatted VAT number in CRM Lead Line and Contract views.
- [#387](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/387) Moved up agents Emails menu entry from Mass Marketing to main menu

## [12.0.1.1.8] - 2021-02-18

### Added
- [#365](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/365) Added OTRS ticket\_number to Contract api, model and form view

### Fixed
- [#380](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/380) Do not allow to create activities through child partners
- [#385](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/385) Mantain the access privileges in the SQL view used by OTRS to read the customers info.

## [12.0.1.1.7] - 2021-02-17

### Changed
- [#367](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/367) Remove context modification to not enqueue jobs in wizard tests, since this is already defined in the `SCTestCase` class from which they inherit.

### Fixed
- [#375](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/375) Disable archive option in contracts and partners for non-admin users
- [#376](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/376) Include reference field to invoice tree view
- [#378](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/378) Make invoice journal name field translatable and add translations

## [12.0.1.1.6] - 2021-02-16

### Added
- [#352](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/352) Add wizard to manually create broadband and mobile crm leads from the partnew form view.

## [12.0.1.1.5] - 2021-02-15

### Added
- [#356](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/356) Add button for download PDF invoice from Open Cell

### Changed
- [#373](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/373) Display Account Move Line name instead of parent's ref to easy match Account Payment Returns
- [#361](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/361) Filled template for unpayed invoice first claim.

### Fixed
- [#368](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/368) Make field member readonly in form partner view
- [#369](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/369) Include phone number to contract tree view
- [#372](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/372) Remove delete and cancel buttons in shares and share subscription tree view

## [12.0.1.1.4] - 2021-02-11

### Fixed
- [#371](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/371) Remove the VAT search in CRMLeadLine views because it generates a bug in the Change email wizard.

## [12.0.1.1.3] - 2021-02-10

### Added
- [#325](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/325) Add "paused" stage in CRMLeadLines and buttons to pause or unpause them. Add filter to select new lines or portability ones, and update the search method to allow searching by multiple attributes from the CRMLeadLine themselfs or their related customers.
- [#355](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/355) Add previous provider constraint when creating broadband-isp-info or mobile-isp-info to check that the given provider has the corresponding (mobile / broadband) service.


### Fixed
- [#353](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/353) Remove sponsor_id relation of Partner when convert to member

## [12.0.1.1.2] - 2021-02-09

### Added
- [#351](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/351) Add error message to the API response in case of exception.
- [#363](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/363) Add service state code to the ServiceData in case of broadband.

### Fixed
- [#359](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/359) Overwrite selection options in type field in SR. Make unnecessary fields invisible from SR form view.

## [12.0.1.1.1] - 2021-02-08

### Added
- [#350](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/350) Add menu entry for emails which can be viewed by agents

### Fixed
- [#357](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/357) Make the automated action "Send email on CRM Lead Line creation" sends emails in background by default
- [#358](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/358) Make country_id not required in partner

## [12.0.1.1.0] - 2021-02-01

### Fixed
- [#354](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/354) Update account-financial-report module to fix trial balance

### Added
- [#266](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/266) Add supplier filters to broadband contract view.


## [12.0.1.0.0] - 2021-02-01

### Added
- [#346](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/346) Add purchase IGIC 7% tax.

### Changed
- [#345](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/345) Hide date done add location mail in create activity popup.

### Fixed
- [#340](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/340) Remove from convert to member wizard the unused company attributes.
- [#343](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/343) Normalize VAT numbers and convert customers NIF/NIE numbers with spanish VAT format.
- [#347](https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests/347) Fix SEPA initiating party identifier.

## [12.0.0.0.0-rc71] - 2021-01-26

All MR can be found in here:
https://gitlab.com/coopdevs/odoo-somconnexio/-/merge_requests?scope=all&utf8=%E2%9C%93&state=merged
