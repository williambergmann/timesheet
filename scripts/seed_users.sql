-- Processing: exportUsers_2026-1-15.csv
-- Found 108 unique users
--   ADMIN: 3
--   STAFF: 104
--   SUPPORT: 1
-- Northstar Timesheet User Seed Data
-- Generated: 2026-01-15T15:49:33.000152
-- Total users: 108

-- Role distribution:
--   ADMIN: 3
--   STAFF: 104
--   SUPPORT: 1

-- Insert users (ON CONFLICT DO NOTHING to avoid duplicates)

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('e6e4c325-0174-4380-b9e2-fb1446349688', 'a9cd273e-509a-4617-b1fa-5ef42dd6a465', 'atoomey@northstar-tek.com', 'Adam Toomey', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('d7bdc6f9-cdc5-4baa-a6a6-203ccf34d9f1', 'aa49ed0d-4b93-48db-89ae-75c03e97bdca', 'adrian@northstar-tek.com', 'Adrian Ratnayake', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('a5a38f21-e688-416d-b62c-88d12bfa1e65', '11ae72bf-8d14-42d4-8723-23deba9bf9d5', 'adriana@northstar-tek.com', 'Adriana Anguiano', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('508e2e18-eb45-4ff5-a0f2-cb1fc4151dd3', '641cc966-3b07-44ab-a081-83ab9f4e0040', 'akashmahajan@northstar-tek.com', 'Akash Mahajan', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('f3b233a8-34d5-4c4c-b08c-1e03723ee16c', '0f4113ce-cd4f-40a4-8ab2-6f13a1414ea3', 'althoreson@northstar-tek.com', 'Al Thoreson', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('3a551501-9b11-4b70-b1d3-a38051902993', 'c46ccb45-2170-4277-9e20-cb0967d2f12f', 'allen.page@northstar-tek.com', 'Allen Page', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('8dfbb678-de28-4608-98c7-eec8ce51e78c', 'aed9edeb-e479-4d56-9134-7fa0354dbe13', 'abundu@northstar-tek.com', 'Alpha Bundu', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('208cc08a-e5e8-4e11-9595-349d0658dc60', '2b9c3e3e-490b-445c-a56f-cfb5ffdd3b4e', 'amber.metz@northstar-tek.com', 'Amber Metz', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('7524d14d-5f34-450d-9b0f-4dd519b9561f', '972915e6-fe37-4577-97a5-3030d9c0bccb', 'aratnayake@northstar-tek.com', 'Amintha Ratnayake', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('a8002564-2f71-4f29-b034-53073129134e', '67c86b19-92aa-430b-86e8-f5ace2b9d7bd', 'andrew.guerrero@northstar-tek.com', 'Andrew Guerrero', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('4d5743f6-9932-4ec8-92e4-281c15fa5178', 'a506da05-6c70-498e-8b30-7ce2003f46dc', 'angel.molina@northstar-tek.com', 'Angel Molina', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('aa5000b1-d4a4-4023-9b03-8aefb845b84c', '5e88e525-d47a-431f-a5a9-c315fa52a385', 'apeterson@northstar-tek.com', 'Austin Peterson', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('47736074-90a5-4d93-a6ff-04771b45e93e', 'be18983d-bc41-4e21-b9e6-393885433169', 'brenda.beltran@northstar-tek.com', 'Brenda Beltran', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('2d12d0c1-4599-4376-bc71-9549b1a1a2f7', '4c91aed2-9a7b-46dc-8fbb-a57a9766b341', 'brett.klooster@northstar-tek.com', 'Brett Klooster', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('104beaff-93d7-4886-b7c6-ef3e755f5848', '1df1cab7-3c7c-4add-b5e7-1f0a4837a585', 'bmartinez@northstar-tek.com', 'Bryan Martinez', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('7d8b5e34-dde7-4e27-9545-36dfb642bcc6', 'ae51f537-f066-4180-bef1-9c3fb5c2fad7', 'ccovington@northstar-tek.com', 'Camaron Covington', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('d0e9a884-9062-49fe-8736-23f03352fe34', '8e3cb0e2-5c9c-4311-a48c-1600954acd5f', 'caroline@northstar-tek.com', 'Caroline Perlstein', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('ee6ef2f4-9dd8-4329-b80d-e84f24fb5796', '4281012b-da61-4d42-8ad4-30604cee1286', 'catkins@northstar-tek.com', 'Chris Atkins', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('ac0fd28c-95b6-4bfc-8346-f555ac9b3b65', '4a72f7eb-6a3f-437f-a6aa-5683a8717732', 'cindy.brown@northstar-tek.com', 'Cindy Brown', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('7b7c6b3d-5f59-4553-b647-18f8511becd0', '91a721d5-5161-40d5-8a9e-b429e4c7312b', 'clipelt@northstar-tek.com', 'Corey Lipelt', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('c24442b6-9cac-47d6-af22-a5dbaf4b5f4e', '66cb6253-683c-4c02-9274-108175f4b967', 'dvonte.muhammad@northstar-tek.com', 'D''vonte Muhammad', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('d49c3af5-c4ac-4029-9cdd-191505a0938f', '123857ee-1689-4b44-b008-1a26c412e434', 'ddombrowski@northstar-tek.com', 'Dane Dombrowski', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('8342c00b-630b-4c95-9b3c-ce0bd25e40b3', 'cce02f97-cbc5-4a81-8646-f87a6f1b69cf', 'dajo@northstar-tek.com', 'Daniel Ajo', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('3fa4b592-07e3-43a0-a859-d3ca60edf157', '87208d47-db12-4e48-a6c4-90d5a7ca7268', 'darius.dotson@northstar-tek.com', 'Darius Dotson', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('7f0b54d6-49d7-40ef-afd3-892d2b01f261', '5a42cf8c-0faa-41f4-8210-85e54419f18a', 'daryl.lindayag@northstar-tek.com', 'Daryl Lindayag', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('fc44ea6e-5093-4cdd-9ba0-20f0611690b7', 'ad2e460d-e4a4-4c3d-88eb-85899c800b10', 'datrell.burris@northstar-tek.com', 'Datrell Burris', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('971d6598-0a2a-47da-9b61-be0ca00f47d5', 'fc49efcd-4e7c-45d8-b092-20e84d52a02b', 'daymond.coleman@northstar-tek.com', 'Daymond Coleman', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('55cd0e15-2b3b-4806-bbd8-452c2658956e', 'c65ec9be-4f6d-417b-a2cc-1545f6c67bec', 'denard.thomas@northstar-tek.com', 'Denard Thomas', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('454b8d80-df27-4d99-af58-263c6131b3c7', '516ee0b3-53f3-464f-b88a-e8c4204bb573', 'dbolanos@northstar-tek.com', 'Derrick Bolanos', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('971c3089-c69e-4e0e-8286-867d0cb99dd7', '31512d45-fc75-4ca4-9b40-059d2e9395fc', 'deven@northstar-tek.com', 'Deven Patterson', 'admin', true, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('90ca0549-603a-4fda-88b2-2cd9c906bc7a', '746a5772-b593-41ba-8aea-5686a73588c2', 'dsimonetti@northstar-tek.com', 'Dominic Simonetti', 'support', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('7cb6e3bb-098b-4cac-abdd-303351a0b622', 'b6451e50-12cc-49bb-96fc-eb27def03da5', 'dquitmeyer@northstar-tek.com', 'Doug Quitmeyer', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('d2483a38-d5c3-426d-9ba1-286375c78226', '14dd797a-03a3-4c2f-910a-0a818821bd55', 'ed.reed@northstar-tek.com', 'Ed Reed', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('ee7be8ee-b234-4b4d-9ff4-c7b8ae9bd9da', 'b61fbf4c-433d-4141-9f51-384cc57762a9', 'ereed@northstar-tek.com', 'Edward Reed', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('d38d7daa-4a30-4942-92d6-8214d17a417c', 'a0df0d8c-aaa8-4794-91f1-1f9a7623bc6f', 'eli.henderson@northstar-tek.com', 'Eli  Henderson', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('c210efd6-4097-4eb8-9b66-2340c8c18798', '79cf2b3d-89a8-43f3-a739-729188f1bb0f', 'ehenderson@northstar-tek.com', 'Eli Henderson', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('f78a03f8-a300-4e9f-b7f6-ea29ac1d394f', 'ef73f0bb-506e-4faa-8288-5ee009b738d9', 'egallegos@northstar-tek.com', 'Elias Gallegos', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('b14c463f-e64a-4d55-a4ff-afc1814a9658', '2319e7fe-6cb7-4fec-a171-3e460bf4b7c3', 'elizabeth.nixon@northstar-tek.com', 'Elizabeth Nixon', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('9121819f-827c-4a76-98df-0bc0024e0c0b', 'a4a4a812-a184-4089-b6ba-d9d36c8bb2e2', 'eric.behrens@northstar-tek.com', 'Eric  Behrens', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('7bf5ce0f-a00f-49b9-8a5d-05be243500f8', '040b7472-b966-4cbe-8d32-023b3e5f47dd', 'ebehren@northstar-tek.com', 'Eric Behrens', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('0670754c-b381-465b-a124-9d1647120ce4', 'f9559038-c3f2-4d02-995e-3802e9baada8', 'enorth@northstar-tek.com', 'Erick North', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('a32579ed-620a-4214-a15d-6d11669a3cca', '12bc0fdf-5a79-4d33-a0fd-3c1beae27647', 'ericka.mooney@northstar-tek.com', 'Ericka Mooney', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('0ef0624c-c970-45a1-8495-9501326a2e6f', '105116f8-5443-4770-a5b9-39f9b77705c6', 'grace@northstar-tek.com', 'Grace Williams', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('53fb33be-c836-4aad-9bd3-bb69ea9ee671', 'c3cacd8d-689b-4086-9ed0-001ec33fdfbc', 'hamam.ismail@northstar-tek.com', 'Hamam Ismail', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('894117ea-0d21-4057-8011-53762c9c1948', 'd37b1632-e580-496a-aec6-b9bc72376b5c', 'hyang@northstar-tek.com', 'Harrison Yang', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('8e7bc099-3407-4883-befd-364267a83659', '64641382-d038-4232-9304-b30f89950a89', 'hallen@northstar-tek.com', 'Helen Allen', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('8842b2a9-be6f-4bba-bbd9-4d6c548a5b77', '48b1b5bb-1c63-4ef0-9e99-c772c1bfeb52', 'ibow@northstar-tek.com', 'Isaiah Bow', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('d87f1ded-45cb-4f60-9780-23b01d746b8c', 'bd948e43-1033-43da-8f46-dae825cf2496', 'jbanks@northstar-tek.com', 'Jacin Banks', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('83606bba-b6df-4914-a177-97c401018c87', '9f5f3b3d-662b-4f7a-b8dd-5b72c273c10f', 'jake.machalec@northstar-tek.com', 'Jake Machalec', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('51fcca7f-d657-445d-94df-6f29a8e52f2c', '386487e0-4f34-4fd4-a977-6e2160178bf2', 'jrosenblatt@northstar-tek.com', 'Jake Rosenblatt', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('644bec3a-62d5-4798-9fc1-f9d2e3c1328d', '1f9d3f7a-a5f3-4230-a233-812d1838b71e', 'jared@northstar-tek.com', 'Jared Peterson', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('c8855e3a-c269-4959-82b0-f695c2833130', '924c5221-1a3a-41be-ad1f-6e1bc2a56528', 'jeff@northstar-tek.com', 'Jeff Elias', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('b5693f12-8238-480c-af3d-a28fd803799d', 'f52d490e-52aa-41b5-8e51-f6c718beca0c', 'jforrest@northstar-tek.com', 'Jeff Forrest', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('4dc417c7-ccbc-4339-8534-bbd0726720e5', '49f78ea9-b8fe-45b3-a497-e01a2558c321', 'jerel.safford@northstar-tek.com', 'Jerel  Safford', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('2497c32f-9756-42d5-a50c-061a3742b0ff', '95e266be-e63b-4aae-b2b7-e0d4599f64fe', 'jpastir@northstar-tek.com', 'Jeremy Pastir', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('9623f6bf-78dd-495d-b531-f2bf72f6455b', '979fa8fe-8d5f-41b8-8716-84d39236e633', 'joel.marquez@northstar-tek.com', 'Joel  Marquez', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('9394b0cb-a5f3-43f7-b4f5-e9a42852e1e2', '3cbc648d-f993-4c63-b580-b04b27d67a09', 'jmarquez@northstar-tek.com', 'Joel Marquez', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('99103e84-dca2-4763-a9a0-c38629952ddb', 'c2f27b46-f6ab-45e2-b5fd-f0b0f1a05d54', 'john.gillroy@northstar-tek.com', 'John Gillroy', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('cc410f80-40ea-41b1-b980-38296586f2f9', '555971c0-cc53-4820-961f-f81e07391916', 'jgilroy@northstar-tek.com', 'John Gilroy', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('ee1243a1-6b21-4fd7-a16b-f58f845624fa', 'ca4a780d-6fb2-44af-8f99-59235f4c1168', 'jcoshway@northstar-tek.com', 'Jon Coshway', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('e7497dc7-ece1-458f-8b51-7cc9963ff713', '7dd58393-09a8-4e50-a2f7-e092534569ad', 'jmills@northstar-tek.com', 'Jonathan Mills', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('15cccb00-ec53-455b-bac6-b03b15b6bed8', '4951813d-6ca9-42db-8b08-d22e972eaf67', 'jscott@northstar-tek.com', 'Josh Scott', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('efea33e0-0f35-49f9-963b-b959e8b96bd8', '8bc923dc-aae7-4a91-b7e3-18a53fbf5083', 'jowens@northstar-tek.com', 'Justin Owens', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('ea30161c-adc5-4e1e-babb-89ab0a489388', '58c132c4-7ffb-4384-b3cd-974ce449c09f', 'kelon.tidwell@northstar-tek.com', 'Kelon Tidwell', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('5cd70264-db9e-4345-ac85-de14f37e2883', 'd0ce6b1e-15b0-45bb-9612-517f61aa21d4', 'kyang@northstar-tek.com', 'Kou Yang', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('a8e9434d-f363-44b8-b131-354946386ead', 'cf4ea5b7-fd1f-480c-985a-65d5a8072bd2', 'kwilia@northstar-tek.com', 'Kris Wilia', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('d116a1df-598c-41fd-9caa-5af2027a7cf7', '9af0b0ce-4f1d-4dd5-a4a8-16a77adcc6bc', 'kristofur.wilia@northstar-tek.com', 'Kristofur Wilia', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('df081685-74d4-4881-b06c-9c6752d190d1', '52fe2788-735d-4290-8c74-feb21d359c57', 'lxiong@northstar-tek.com', 'Lucas Xiong', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('b2bca2e9-26df-494f-8c1c-b4015cb76a40', 'd393bfe9-6e99-4d84-b372-c92b46b1bb1d', 'ltheriot@northstar-tek.com', 'Luke Theriot', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('e1ce2e1d-d0f8-4e32-adc1-5b19985f2294', '9430871a-04dc-4a0c-8355-2d927da2c2bc', 'megan@northstar-tek.com', 'Megan Patterson', 'admin', true, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('42e8ab5a-a051-470f-b6d9-3f95ce17b906', '8aec6eca-af81-4bac-903c-29b6d6c5335c', 'melissa@northstar-tek.com', 'Melissa Skow', 'admin', true, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('ba44bf6a-ddd9-473c-97d2-d45288232fb9', '7f5727a2-93d6-4d49-8216-7d99f26905d9', 'mgerber@northstar-tek.com', 'Michael Gerber', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('65042c79-54d2-44a0-a496-2a59b59e7998', 'f84321ed-70cf-43ba-83bb-304565f588eb', 'mpargas@northstar-tek.com', 'Michael Pargas', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('1b6fe45d-093a-4b7f-aee0-b300d3ac7d19', '70cdafa7-1a28-48d0-968b-8d64ff4e03ad', 'myang@northstar-tek.com', 'Michael Yang', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('1e2a433f-de51-4ab7-9283-d7fba124d905', '2f28bb13-25f6-4b5a-a120-d07c193b357c', 'michelle@northstar-tek.com', 'Michelle Ratnayake', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('db4e988f-fa6a-402f-91e1-68617649d7fe', '6c769239-3de3-45f6-be5b-610fbf88e333', 'mike.brown@northstar-tek.com', 'Mike  Brown', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('327524c8-5bb4-445c-84c9-2803c8e376ba', 'c104fe57-8ef9-4f8d-9d87-4bb364014f3a', 'mbrown@northstar-tek.com', 'Mike Brown', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('f66aeb17-9e6c-4c38-838e-7d3e4dc61f63', '41ec64b2-c620-42bf-8f12-1744aa1869b6', 'msmith@northstar-tek.com', 'Mike Smith', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('6523ebdd-5db8-406e-8228-391fa4315894', 'e99aec8d-05ce-4db7-b9db-0ec0b349c72f', 'msledge@northstar-tek.com', 'Mitch Sledge', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('a97fd271-3b1f-4aa5-bc18-098d62b52a84', '7bd20b28-1602-4c2d-82ea-cc52c193d9d5', 'nmohamoud@northstar-tek.com', 'Nasir Mohamoud', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('8ab12dda-cbb7-48c0-96fc-03586f3d134f', 'bf992936-ed5a-48fb-9264-48f76b57f600', 'nscott@northstar-tek.com', 'Nick Scott', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('6a14d360-e252-441b-8d04-3a3ac6bfc460', '96c5a11e-f3af-4837-8467-270ab1980d02', 'ncoons@northstar-tek.com', 'Nicolas Coons', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('414d7580-6dff-4306-8dd6-e02abea3a6ec', '3f252d32-99bd-4638-801e-34dfa983bb37', 'omar.benazza@northstar-tek.com', 'Omar Benazza', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('9fb8249c-246f-44f2-8b5e-5ed8b13269cb', '11a1321c-4788-4e26-bd49-64d2bb2e2de0', 'ocovarrubias@northstar-tek.com', 'Omar Covarrubias', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('fc73498b-e720-489a-8df3-2b3562e13d2d', '86e74500-b897-47ad-b40c-768d697e1b86', 'owen.white@northstar-tek.com', 'Owen White', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('3ec5c96d-b0d8-48d8-b7de-347d63be7589', '5eb74ff1-c806-46c0-9ba1-d9d3ac0fdc32', 'phayes@northstar-tek.com', 'Patrick Hayes', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('503763b4-e945-4bae-8aa9-8037a54622f3', 'cc129a56-4818-4075-9bb6-96e86e8b0224', 'pschoonover@northstar-tek.com', 'Patrick Schoonover', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('215a371a-0bc9-4a75-b81a-5c018d89c6ae', 'a0d83146-75c1-4997-948e-5c79a6aa4e4d', 'paul.bell@northstar-tek.com', 'Paul Bell', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('5619b630-0b8b-4a27-8734-61ea5f8d5b40', '44a88fab-4739-46a0-8c52-33f2d3a310c2', 'pbell@northstar-tek.com', 'Paull Bell', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('c9b98464-b4f8-4c3c-b0c2-ab9ac3b1577c', '2cfa29f8-28e6-4068-b802-54177883c265', 'rmorrow@northstar-tek.com', 'Ryan Morrow', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('c2e1d597-df19-4150-9e5b-2197afa184c1', '2627194f-9cf7-4738-ad38-2224dbfb5d7a', 'schisholm@northstar-tek.com', 'Sam Chisholm', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('9cd841a3-a3c5-449d-a308-b220e5d81964', '1cd95a9b-95ad-46d7-b4a3-cd4d79200a84', 'sjohnson@northstar-tek.com', 'Scott Johnson', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('de0af3a4-0562-4ba3-b129-bceac7de7028', '754539b9-aeba-49fa-adac-12aa7ff8b98c', 'sligas@northstar-tek.com', 'Simon Ligas', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('d7fb6e12-fde0-4953-9e24-d4675e53df16', '14537eb2-ee5c-41b5-927d-ec1573516a02', 'stephen.dickey@northstar-tek.com', 'Stephen Dickey', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('7885590e-6d7e-4eea-a342-a4f5b6d66785', '9b549105-0832-44ee-8813-4ab1fd8dc0ff', 'steve.heitkamp@northstar-tek.com', 'Steve Heitkamp', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('c9154e28-11c8-4aa8-95e6-676be00ba5c5', '73e6bd2f-69da-4344-96e0-f75882d84f0c', 'tvue@northstar-tek.com', 'Tim Vue', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('638e728a-62d5-4179-a78f-e12225ecbb73', '9f79f385-db65-4188-8a24-ca28593c3df4', 'tomking@northstar-tek.com', 'Tom King', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('5185939f-9498-4e40-99c2-5f3fcf83f589', '5b1a384b-ce1b-4afc-8b5b-cd536e2c4fd9', 'trent@northstar-tek.com', 'Trent Nwogwugwu', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('3bf8fc16-4ba7-462c-ace3-981c02559a0f', 'cc0b645a-fb6e-4919-9f37-c8c5d473394c', 'tboland@northstar-tek.com', 'Tyler Boland', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('905834c2-7d64-491c-a372-2e85f80e598d', 'fbf01f8a-c7c4-4092-a534-46dc9b05d224', 'vjohnson@northstar-tek.com', 'Victor Johnson', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('f17bd981-f3f0-49f4-9630-0b5b894d40df', '19391e16-58ec-40fd-be8b-2c397ba6e2ca', 'wbergmann@northstar-tek.com', 'WILLIAM BERGMANN', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('af5700bc-2b0c-48d7-ba5d-d4275d3bd91c', '173bf08d-5079-4721-8bf4-be13b469ae8c', 'weissa@northstar-tek.com', 'Waleed Eissa', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('6c3e8613-50ab-4f64-a0c8-4168baf2fa2b', '281ac94d-007d-48d2-b4b3-a8cb5a41cb8f', 'wally.barry@northstar-tek.com', 'Wally Barry', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('42439c72-dbd1-465c-a2c2-1bae9daa7e04', '28bec712-1e77-4d57-9532-5575cd317744', 'william.bergmann@northstar-tek.com', 'William  Bergmann', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('f3c735df-c96d-499e-b3d7-788dccb7d224', 'e223b7dc-6372-4ee9-8c76-77f11201485f', 'wdiaz@northstar-tek.com', 'William Diaz', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('71ffabcf-12d6-412e-b445-3abfaca75937', '03be5a15-78a1-4e1e-871d-ff18e62b6c6d', 'william.thornton@northstar-tek.com', 'William Thornton', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('84a9198b-c2d7-4055-8c90-cf80f463d6ea', '3cf8fba1-19fa-42ab-9b7f-26a89d0372e6', 'xdavis@northstar-tek.com', 'Xavier Davis', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('609217b3-cc2f-4499-8866-907b1cd1cfb6', '3382edf8-34e9-4688-be76-0271f2bb095c', 'bbauer@northstar-tek.com', 'benjamin bauer', 'staff', false, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

