document.addEventListener("DOMContentLoaded", function () {
    const emailInput = document.getElementById("titular_email");
    const confirmEmailInput = document.getElementById("titular_confirm_email");
    const ibanInput = document.getElementById("iban");
    const nifInput = document.getElementById("titular_nif");
    const cupsInput = document.getElementById("cups");
    const serviceZipCodeInput = document.getElementById("service_zip_code");
    const titularZipCodeInput = document.getElementById("titular_zip_code");
    const phoneInput = document.getElementById("titular_phone");
    const cauInput = document.getElementById("cau");
    const refCadastralInput = document.getElementById("cadastral_reference");
  
    function validateEmailMatch(email, confirmEmail) {
      return email.trim() === confirmEmail.trim();
    }
  
    function validateIBAN(iban) {
      iban = iban.replace(/\s+/g, '').toUpperCase();
      const regex = /^ES\d{22}$/;
      return regex.test(iban);
    }
  
    function validateNIF(nif) {
      const nifRegex = /^[XYZ]?[0-9]{7,8}[A-Z]$/i;
      return nifRegex.test(nif);
    }
  
    function validateCUPS(cups) {
      cups = cups.toUpperCase().replace(/\s+/g, '');
      return /^ES[0-9]{16}[A-Z0-9]{2}$/.test(cups);
    }
  
    function validatePostalCode(cp) {
      cp = cp.trim();
      if (!/^\d{5}$/.test(cp)) return false;
      const province = parseInt(cp.substring(0, 2), 10);
      return province >= 1 && province <= 52;
    }
  
    function validateSpanishMobile(phone) {
      phone = phone.replace(/\s+/g, '').trim();
      return /^[67]\d{8}$/.test(phone);
    }
  
    function validateFixedLengthAlphanumeric(value, length, allowEmpty = false) {
      value = value.toUpperCase().replace(/\s+/g, '');
      if (allowEmpty && value === '') return true;
      const regex = new RegExp(`^[A-Z0-9]{${length}}$`);
      return regex.test(value);
    }
  
    function attachValidation(input, validateFn) {
      function check() {
        const valid = validateFn(input.value);
        input.classList.remove("is-valid", "is-invalid");
        if (input.value.trim() !== '' || !validateFn('', true)) {
          input.classList.add(valid ? "is-valid" : "is-invalid");
        }
        return valid;
      }
      input.addEventListener("input", check);
      return check;
    }
  
    const validators = [
      () => {
        const valid = validateEmailMatch(emailInput.value, confirmEmailInput.value);
        [emailInput, confirmEmailInput].forEach(input => {
          input.classList.remove("is-valid", "is-invalid");
          input.classList.add(valid ? "is-valid" : "is-invalid");
        });
        return valid;
      },
      attachValidation(ibanInput, validateIBAN),
      attachValidation(nifInput, validateNIF),
      attachValidation(cupsInput, validateCUPS),
      attachValidation(serviceZipCodeInput, validatePostalCode),
      attachValidation(titularZipCodeInput, validatePostalCode),
      attachValidation(phoneInput, validateSpanishMobile),
      attachValidation(cauInput, value => validateFixedLengthAlphanumeric(value, 36, true)),
      attachValidation(refCadastralInput, value => validateFixedLengthAlphanumeric(value, 20, true))
    ];
  
    document.querySelector("form").addEventListener("submit", function (event) {
      let allValid = true;
      validators.forEach(validate => {
        if (!validate()) {
          allValid = false;
        }
      });
      if (!allValid) {
        event.preventDefault();
      }
    });
  });
  