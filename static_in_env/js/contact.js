$(document).ready(function () {
  contactForm();
});

function disableForm($form, isDisabled) {
  $form.find("input, textarea, select, button").each(function (index, element) {
    $(element).prop("disabled", isDisabled);
  });
}

function contactForm() {
  var $element = $(".js-form-contact");
  if (!$element.length) {
    return;
  }

  $element.validate({
    rules: {
      name: {
        required: true,
        minlength: 3,
      },
      company: {
        required: true,
      },
      email: {
        email: true
      },
      message: {
        required: false,
        minlength: 10
      },
      phone: {
        required: false,
        phone: true
      },
      agree: "required"
    },
    messages: {
      name: {
        required: tbp_data_contact.form_contact.name.required,
        minlength: tbp_data_contact.form_contact.name.minlength,
      },
      company: {
        required: tbp_data_contact.form_contact.company.required
      },
      email: {
        required: tbp_data_contact.form_contact.email.required
      },
      phone: {
        required: tbp_data_contact.form_contact.phone.required
      },
      message: {
        required: tbp_data_contact.form_contact.message.required,
        minlength: tbp_data_contact.form_contact.message.minlength,
      },
      agree: tbp_data_contact.form_contact.agree.required
    },
    submitHandler: function (form) {
      var $form = $(form);
      var $btnSubmitText = $form.find("button[type='submit']").find(".btn__text");
      var $formFeedback = $form.find(".js-form-feedback");
      var formValues = $form.serializeArray();
      var formData = {};
      $.each(formValues, function () {
        formData[this.name] = this.value;
      });

      $.ajax({
        url: tbp_data_settings.ajax_url,
        method: "POST",
        data: {
          action: "tbp-contact",
          _ajax_nonce: tbp_data_contact._ajax_nonce,
          form: formData
        },
        beforeSend: function() {
          disableForm($form, true);
          $btnSubmitText.text(tbp_data_contact.form_contact.submitting);
          $formFeedback.text("");
          $formFeedback.addClass("d-none");
        },
        success: function(response) {
          if(response.success) {
            disableForm($form, true);
            var modalContactEl = document.getElementById("modal-contact");
            if(!modalContactEl) {
              return;
            }
            var modalContact = bootstrap.Modal.getInstance(modalContactEl);
            modalContactEl.addEventListener("hidden.bs.modal", function (event) {
              if(response.success) {
                var modalSuccessEl = document.getElementById("modal-success");
                if(!modalSuccessEl) {
                  return;
                }
                var modalSuccess = new bootstrap.Modal(modalSuccessEl);
                modalSuccess.show();
              }
            });
            modalContact.hide();
            $btnSubmitText.text(tbp_data_contact.form_contact.submitted);
          } else {
            disableForm($form, false);
            $btnSubmitText.text(tbp_data_contact.form_contact.submit);
            var dataLength = response.data.length;
            var text = array();
            for(var i = 0; i < dataLength; i++) {
              text.push(response.data[i]);
            }
            $formFeedback.text(text.join("<br>"));
            $formFeedback.removeClass("d-none");
          }
        },
        error: function(response) {
          disableForm($form, false);
          $btnSubmitText.text(tbp_data_contact.form_contact.submit);
        }
      });

      return false;
    },
    invalidHandler: function (e, validator) {
    }
  });
}