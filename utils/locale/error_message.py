def get_error_message(language="en", error_type="failed", **kwargs):

    try:
        error_messages = {
            "en": {
                "failed": "Request failed",
                "invalid_request": "Invalid request",
                "invalid_plan_id": "Invalid plan id",
                "invalid_number_of_credits": "Invalid number of credits",
                "user_number_of_credits": f"You have {kwargs['no_of_credits']} credit(s) left",
                "number_of_credits_must_be_between_1_to_10": "Number of credits must be between 1 to 10",
                "not_enough_credits": "Not enough credits",
                "user_not_found": "User not found",
                "invalid_payload": "Invalid payload",
                "invalid_signature": "Invalid signature",
                "user_not_found": "User not found",
                "password_updated_successfully": "Password updated successfully",
                "user_profile_updated_successfully": "User profile updated successfully"
            },
            "tr": {
                "failed": "İstek başarısız",
                "invalid_request": "Geçersiz istek",
                "invalid_plan_id": "Geçersiz plan id",
                "invalid_number_of_credits": "Geçersiz kredi sayısı",
                "user_number_of_credits": f"Kalan {kwargs['no_of_credits']} krediniz var",
                "number_of_credits_must_be_between_1_to_10": "Kredi sayısı 1 ile 10 arasında olmalıdır",
                "not_enough_credits": "Yeterli kredi yok",
                "user_not_found": "Kullanıcı bulunamadı",
                "invalid_payload": "Geçersiz veri",
                "invalid_signature": "Geçersiz imza",
                "user_not_found": "Kullanıcı bulunamadı",
                "password_updated_successfully": "Şifre başarıyla güncellendi",
                "user_profile_updated_successfully": "Kullanıcı profiliniz başarıyla güncellendi"
            },
            "fa": {
                "failed": "درخواست ناموفق",
                "invalid_request": "درخواست نامعتبر",
                "invalid_plan_id": "شناسه طرح نامعتبر است",
                "invalid_number_of_credits": "تعداد اعتبار نامعتبر است",
                "user_number_of_credits": f"شما {kwargs['no_of_credits']} اعتبار دارید",
                "number_of_credits_must_be_between_1_to_10": "تعداد اعتبار باید بین 1 تا 10 باشد",
                "not_enough_credits": "اعتبار کافی نیست",
                "user_not_found": "کاربر یافت نشد",
                "invalid_payload": "داده نامعتبر",
                "invalid_signature": "امضای نامعتبر",
                "user_not_found": "کاربر یافت نشد",
                "password_updated_successfully": "رمز عبور با موفقیت به روز شد",
                "user_profile_updated_successfully": "پروفایل کاربری با موفقیت به روز شد"
            }
        }

        return error_messages[language][error_type]
    except:
        return "Request failed"
