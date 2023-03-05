const pages = {
  Index: "Dashboard/Index.vue",

  Login: "Auth/Login.vue",
  Register: "Auth/Register.vue",
  ConfirmEmail: "Auth/ConfirmEmail.vue",
  EmailVerificationSend: "Auth/EmailVerificationSend.vue",
  PasswordReset: "Auth/PasswordReset.vue",
  SetPasswordFromKey: "Auth/SetPasswordFromKey.vue",

  SettingsIndex: "Settings/General/Index.vue",
  ChangePassword: "Settings/Auth/ChangePassword.vue",

  "400Error": "Errors/400.vue",
  "403Error": "Errors/403.vue",
  "404Error": "Errors/404.vue",
  "500Error": "Errors/500.vue",

  Users: "Management/Users/List.vue",
  UserDetail: "Management/Users/Detail.vue",
  UserCreate: "Management/Users/Create.vue",

  SystemSettingsGeneral: "System/General/Index.vue",
  SystemSettingsSecurity: "System/Security/Index.vue",
  SystemSettingsScripts: "System/Scripts/Index.vue",
};

export default pages;
