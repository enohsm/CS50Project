SELECT
    visa.country,
    visa.visa_type,
    visa.prefferred_appointment_date AS pref_date,
    visa.status AS stat,
    visa.request_date,
    visa.payment_status AS payment,
    visa.appointment_date AS app_date,
    visa.result_date,
    user.username,
    pass.name,
    pass.surname,
    pass.pass_no
FROM visa_requests AS visa
JOIN users AS user
    ON visa.user_id = user.id
JOIN passports AS pass
    ON visa.pass_id = pass.id