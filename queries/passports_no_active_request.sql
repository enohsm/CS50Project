SELECT DISTINCT
    passports.pass_no AS pass_no,
    passports.pass_exp AS pass_exp
FROM passports
LEFT JOIN visa_requests
    ON passports.id = visa_requests.pass_id
WHERE passports.user_id = ?
    AND (visa_requests.status != 1 AND visa_requests.status != 0 OR visa_requests.status IS NULL)
    AND passports.confirmed != 0