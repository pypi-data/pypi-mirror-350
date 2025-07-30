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
    const firstnameInput = document.getElementById("titular_firstname");
    const lastnameInput = document.getElementById("titular_lastname");
    const serviceCityInput = document.getElementById("service_city");
    const titularCityInput = document.getElementById("titular_city");
  
    function validateEmailMatch(email, confirmEmail) {
      return email.trim() === confirmEmail.trim();
    }
  
    function validateIBAN(iban) {
      iban = iban.toUpperCase().trim().replace(/\s/g, "");
  
      if (iban.length !== 24) return false;
  
      const letter1 = iban.charAt(0);
      const letter2 = iban.charAt(1);
      const num1 = getIBANCharValue(letter1);
      const num2 = getIBANCharValue(letter2);
  
      let transformed = String(num1) + String(num2) + iban.slice(2);
      transformed = transformed.slice(6) + transformed.slice(0, 6);
  
      return calculateMod97(transformed) === 1;
    }
    
    function calculateMod97(input) {
      const parts = Math.ceil(input.length / 7);
      let remainder = "";
      for (let i = 0; i < parts; i++) {
          remainder = String(parseFloat(remainder + input.substr(i * 7, 7)) % 97);
      }
      return parseInt(remainder, 10);
    }
    
    function getIBANCharValue(char) {
      const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
      return alphabet.indexOf(char) + 10;
    }
  
    function validateNIF(nif) {
      const nifRegex = /^[XYZ]?\d{5,8}[A-Z]$/;
      nif = nif.toUpperCase();
  
      if (!nifRegex.test(nif)) {
          return false;
      }
  
      let number = nif.slice(0, -1).replace('X', '0').replace('Y', '1').replace('Z', '2');
      const expectedLetter = 'TRWAGMYFPDXBNJZSQVHLCKET'.charAt(parseInt(number, 10) % 23);
      const actualLetter = nif.slice(-1);
  
      return expectedLetter === actualLetter;
    }
    
    function validateCUPS(CUPS) {
      let ret = false;
      const reCUPS = /^[A-Z]{2}(\d{4}\d{12})([A-Z]{2})(\d[FPCRXYZ])?$/i;
      if (reCUPS.test(CUPS)) {
        const mCUPS = CUPS.toUpperCase().match(reCUPS);
        const [, cups16, control] = mCUPS;
        const letters = [
          'T', 'R', 'W', 'A', 'G', 'M',
          'Y', 'F', 'P', 'D', 'X', 'B',
          'N', 'J', 'Z', 'S', 'Q', 'V',
          'H', 'L', 'C', 'K', 'E',
        ];
    
        const cup16Mod = +cups16 % 529,
          quotient = Math.floor(cup16Mod / letters.length),
          remainder = cup16Mod % letters.length;
    
        ret = (control === letters[quotient] + letters[remainder]);
      }
    
      return ret;
    }
  
    function validatePostalCode(cp) {
      cp = cp.trim();
      if (!/^\d{5}$/.test(cp)) return false;
      const province = parseInt(cp.substring(0, 2), 10);
      return province >= 1 && province <= 52;
    }
  
    function validateSpanishPhone(phone) {
      phone = phone.replace(/\s+/g, '').trim();
      return /^[6789]\d{8}$/.test(phone);
    }    
  
    function validateFixedLengthAlphanumeric(value, length, allowEmpty = false) {
      value = value.toUpperCase().replace(/\s+/g, '');
      if (allowEmpty && value === '') return true;
      const regex = new RegExp(`^[A-Z0-9]{${length}}$`);
      return regex.test(value);
    }

    function isValidTextOnly(input) {
      const regex = /^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$/;
      return regex.test(input.trim());
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
      attachValidation(phoneInput, validateSpanishPhone),
      attachValidation(cauInput, value => validateFixedLengthAlphanumeric(value, 36, true)),
      attachValidation(refCadastralInput, value => validateFixedLengthAlphanumeric(value, 20, true)),
      attachValidation(firstnameInput, isValidTextOnly),
      attachValidation(lastnameInput, isValidTextOnly),
      attachValidation(serviceCityInput, isValidTextOnly),
      attachValidation(titularCityInput, isValidTextOnly)
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
  