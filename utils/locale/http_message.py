def get_http_message(language="en", http_type="failed", **kwargs):

    try:
        http_messages = {
            "en": {
                "failed": "Request failed",
                "invalid_request": "Invalid request",
                "invalid_body_request": "Missing or invalid field in JSON body",
                "invalid_plan_id": "Invalid plan id",
                "invalid_number_of_credits": "Invalid number of credits",
                "user_number_of_credits": f"You have {kwargs.get('no_of_credits')} credit(s) left",
                "number_of_credits_must_be_between_1_to_10": "Number of credits must be between 1 to 10",
                "not_enough_credits": "Not enough credits",
                "user_not_found": "User not found",
                "user_already_exists": "User with this email already exists",
                "invalid_payload": "Invalid payload",
                "invalid_signature": "Invalid signature",
                "password_updated_successfully": "Password updated successfully",
                "user_profile_updated_successfully": "User profile updated successfully",
                "user_personal_info_updated_successfully": "User personal info updated successfully",
            },
            "tr": {
                "failed": "İstek başarısız",
                "invalid_request": "Geçersiz istek",
                "invalid_body_request": "JSON verisinde eksik veya geçersiz alan",
                "invalid_plan_id": "Geçersiz plan id",
                "invalid_number_of_credits": "Geçersiz kredi sayısı",
                "user_number_of_credits": f"Kalan {kwargs.get('no_of_credits')} krediniz var",
                "number_of_credits_must_be_between_1_to_10": "Kredi sayısı 1 ile 10 arasında olmalıdır",
                "not_enough_credits": "Yeterli kredi yok",
                "user_not_found": "Kullanıcı bulunamadı",
                "user_already_exists": "Bu e-posta ile kullanıcı zaten mevcut",
                "invalid_payload": "Geçersiz veri",
                "invalid_signature": "Geçersiz imza",
                "password_updated_successfully": "Şifre başarıyla güncellendi",
                "user_profile_updated_successfully": "Kullanıcı profiliniz başarıyla güncellendi",
                "user_personal_info_updated_successfully": "Kullanıcı kişisel bilgileriniz başarıyla güncellendi",
            },
            "fa": {
                "failed": "درخواست ناموفق",
                "invalid_request": "درخواست نامعتبر",
                "invalid_body_request": "فیلد از بدنه جیسون گم شده یا نامعتبر است",
                "invalid_plan_id": "شناسه طرح نامعتبر است",
                "invalid_number_of_credits": "تعداد اعتبار نامعتبر است",
                "user_number_of_credits": f"شما {kwargs.get('no_of_credits')} اعتبار دارید",
                "number_of_credits_must_be_between_1_to_10": "تعداد اعتبار باید بین 1 تا 10 باشد",
                "not_enough_credits": "اعتبار کافی نیست",
                "user_not_found": "کاربر یافت نشد",
                "user_already_exists": "کاربر با این ایمیل از پیش وجود دارد",
                "invalid_payload": "داده نامعتبر",
                "invalid_signature": "امضای نامعتبر",
                "password_updated_successfully": "رمز عبور با موفقیت به روز شد",
                "user_profile_updated_successfully": "پروفایل کاربری با موفقیت به روز شد",
                "user_personal_info_updated_successfully": "اطلاعات شخصی کاربر با موفقیت به روز شد",
            }
        }

        return http_messages[language][http_type]
    
    except Exception as e:
        print('e', e)
        return "Request failed"
