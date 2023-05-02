class States:
  REGISTER = {0 : 'register_start',
              1 : 'register_input',
              2 : 'register_selection'}
  
  MAIN_MENU = 'main_menu'
  SCHEDULE_MENU = 'schedule_menu'
  MARKS_MENU = 'marks_menu'
  MAILING_MENU = 'mailing'
  
  EDIT_CONF = {0 : 'edit_config_start',
              1 : 'edit_config_input',
              2 : 'edit_config_selection'}
  
  RUOBR_REGISTER = {0 : 'ruobr_register_start',1 : 'ruobr_register_login',2 : 'ruobr_register_password',3 : 'ruobr_register_selection'}

  PREDICTION_MENU = 'prediction'

  PARAMETERS_MENU = 'parameters'
  
  EXCEL_MENU = 'excel_menu'