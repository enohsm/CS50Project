SELECT *
FROM passports
JOIN visa_requests
    ON passports.id = visa_requests.pass_id
WHERE passports.user_id = ?
    AND passports.id = ?
    AND visa_requests.status != 3