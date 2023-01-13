# -barcode-recognition
Телеграмм бот, распознает штрихкоды с фотографии и присылает информацию из базы данных.
Бот раз в пол часа обновляет БД, данные берет из файлаcel Excel, соответсвенно можно настрогить выгрузку файлов из 1С или битрикс и бот будет работать автономно.
При запуске бота нужно только указать название файла из которого он будет брать данные, бот использует модуль Threading, чтобы обновление БД проходило параллельно работе самого бота
Telegram bot recognizes barcodes from photos and sends information from the database.
The bot updates the database every half an hour, takes the data from the Excel file, respectively, you can set up uploading files from 1C or Bitrix and the bot will work offline.
When starting the bot, you only need to specify the name of the file from which it will take data, the bot uses the Threading module so that the database update takes place in parallel with the work of the bot itself
