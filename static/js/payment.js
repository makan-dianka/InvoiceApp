// style css 
var style = {
    base : {
        color: '#32325d',
        fontFamily: "helvetica sans-serif",
        fontSmoothing: "antialiased",
        fontSize: "14px",
        '::placeholder': {
            color: "#aab7c4",
        }
    },
    invalid: {
        color: "#fa755a",
        iconColor: "#fa755a",
    }
  }
  
document.addEventListener('DOMContentLoaded', async () => {

    // get stripe public key
    const configScript = document.getElementById('stripe-config');
    const stripePublicKey = configScript.getAttribute('data-stripe-key');

    const stripe = Stripe(stripePublicKey)
    const elements = stripe.elements()
    var card = elements.create("card", {style: style});
    card.mount("#card-element");
  
    card.addEventListener('change', function(event){
      var displayError=document.getElementById("card-errors")
      if (event.errors) {
          displayError.textContent = event.error.message
      }else{
          displayError.textContent = ''
      }
    })

// create stripe token
var form = document.getElementById("payment-form")
    form.addEventListener('submit', function(event){
        event.preventDefault()
        stripe.createToken(card).then(function(result){
            if (result.error) {
                var errorElement = document.getElementById("card-errors")
                errorElement.textContent = result.error.message
            }else{
                stripeTokenHandler(result.token)

                // spinner
                const btn = document.getElementById('btn-payer');
                const spinner = document.getElementById('btn-spinner');
                const overlay = document.getElementById('overlay-spinner');

                spinner.classList.remove('d-none');

                // deactivate btn payment
                btn.disabled = true;

                // show spinner on full screen
                overlay.classList.remove('d-none');

            }
        })
    })
  
// append stripe token to the form 
function stripeTokenHandler(token){
    var form = document.getElementById("payment-form")
    var hiddenInput = document.getElementById("input")
    hiddenInput.setAttribute('name', 'stripeToken')
    hiddenInput.setAttribute('value', token.id)
    form.appendChild(hiddenInput)
    form.submit()
    }

  })