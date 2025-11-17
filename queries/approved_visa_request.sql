SELECT 
    visa.id,
    visa.pass_id,
    visa.country,
    pass.name,
    pass.surname,
    pass.pass_no,
    visa.appointment_date AS app_date
FROM visa_requests AS visa
JOIN passports AS pass
    ON visa.pass_id = pass.id
WHERE visa.status = 1
    AND visa.id = ?
ORDER BY visa.request_date