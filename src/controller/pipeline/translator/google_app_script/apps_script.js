function doPost(e) {
    console.log(e)

    var error = null;
    var translate = null;
    if (typeof e.parameter.source_lang == 'undefined') {
      str = 'source_lang is required'
    } else if (typeof e.parameter.target_lang == 'undefined') {
      str = 'target_lang is required'
    } else if (typeof e.parameter.text == 'undefined') {
      error = 'text is required'
    } else {
      var source_lang = e.parameter.source_lang.trim();
      var target_lang = e.parameter.target_lang.trim();
      var text = e.parameter.text.trim();

      source_lang = source_lang === 'auto' ? '' : source_lang;
      try {
        translate = LanguageApp.translate(text, source_lang, target_lang);
      } catch (err) {
        error = err.message;
      }
    }

    var result = JSON.stringify(error == null ? {
      'status': 'ok',
      'translated': translate,
      'req':e.parameter.text
    } : {
      'status': 'error',
      'message': error
    })

    return ContentService.createTextOutput(result)
  }
