SELECT 
    visa.id,
    visa.country,
    pass.name,
    pass.surname,
    pass.pass_no,
    pass.sex,
    visa.visa_type,
    pass.pass_exp,
    visa.prefferred_appointment_date AS pref_date,
    visa.status AS stat,
    visa.request_date,
    visa.payment_status AS payment
FROM visa_requests AS visa
JOIN passports AS pass
    ON visa.pass_id = pass.id
WHERE visa.status = 0
ORDER BY visa.request_date