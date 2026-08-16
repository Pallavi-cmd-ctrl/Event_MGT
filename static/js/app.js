document.querySelector('.nav-toggle')?.addEventListener('click', () => document.querySelector('.nav-links').classList.toggle('open'));
document.querySelectorAll('input[type="date"]').forEach(input => { if (!input.min) input.min = new Date().toISOString().split('T')[0]; });
const paymentMethods = document.querySelectorAll('input[name="payment_method"]');
const cardFields = document.querySelector('[data-payment-fields="card"]');
const upiFields = document.querySelector('[data-payment-fields="upi"]');
const payButton = document.querySelector('[data-pay-button]');
paymentMethods.forEach(method => method.addEventListener('change', () => { const isUpi = method.value === 'upi' && method.checked; if (cardFields) { cardFields.hidden = isUpi; cardFields.querySelectorAll('input').forEach(input => { input.disabled = isUpi; input.required = !isUpi; }); } if (upiFields) { upiFields.hidden = !isUpi; upiFields.querySelector('input').disabled = !isUpi; upiFields.querySelector('input').required = isUpi; } if (payButton) payButton.textContent = payButton.textContent.replace(isUpi ? 'by Card' : 'by UPI', isUpi ? 'by UPI' : 'by Card'); }));
