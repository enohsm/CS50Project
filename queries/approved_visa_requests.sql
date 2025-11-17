SELECT 
    visa.id,
    visa.country,
    pass.name,
    pass.surname,
    pass.pass_no,
    visa.status AS stat,
    visa.request_date,
    visa.appointment_date AS app_date
FROM visa_requests AS visa
LEFT JOIN passports AS pass
    ON visa.pass_id = pass.id
WHERE visa.status = 1
ORDER BY visa.request_date