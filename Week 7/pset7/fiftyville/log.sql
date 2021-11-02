-- Keep a log of any SQL queries you execute as you solve the mystery.

-- To know the crime scene report and grab information
SELECT description FROM crime_scene_reports WHERE day = 28 AND street = "Chamberlin Street";

-- Interviews about the theft
SELECT name, transcript FROM interviews WHERE day = 28 AND month = 7 AND year = 2020;

-- Cars who left the courthouse from 10:00 to 10:25
SELECT minute, license_plate, activity FROM courthouse_security_logs WHERE month = 7 AND day = 28 AND hour >= 10 AND minute <= 25 ORDER BY minute;

-- Fifer Street's ATM transactions for each account
SELECT account_number, amount, transaction_type, atm_location FROM atm_transactions WHERE month = 7 AND day = 28;

-- Less-than-a-minute calls
SELECT DISTINCT(caller), receiver, duration FROM phone_calls WHERE month = 7 AND day = 28 AND year = 2020 AND duration <= 60;

-- Id and name of the cities
SELECT id, city FROM airports;

-- Fiftyville is city 8. The earliest flight is to city 4 (London) at 08:20. Flight 36.
SELECT id, destination_airport_id, hour, minute FROM flights WHERE origin_airport_id = 8 AND day = 29 AND month = 7 AND year = 2020;

-- To know who (1) exit the courthouse, (2) made a less than a minute call and (3) was on flight 36
SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36) AND license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE month = 7 AND day = 28 AND hour >= 10 AND minute <= 25) AND phone_number IN (SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND year = 2020 AND duration <= 60);

-- Persons of interest: Roger, Evelyn, Ernest

-- Who from the suspects withdraw money from Fifer Street?
SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36) AND id IN (SELECT person_id FROM bank_accounts WHERE account_number IN(SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw"));
-- Only Ernest from the list of suspects was there.

-- Ernest's phone number: (367) 555-5533
SELECT phone_number FROM people WHERE name = "Ernest";

-- Who did he call to?
SELECT name FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE caller = "(367) 555-5533" AND month = 7 AND day = 28 AND year = 2020 AND duration <= 60);
-- Berthold.