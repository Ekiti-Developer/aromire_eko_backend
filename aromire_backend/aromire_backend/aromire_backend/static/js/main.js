/**
 * Aromire-Èko Empowerment Foundation
 * Contact form handler
 */

/**
 * Handle contact form submission with visual feedback.
 * @param {Event} e - The form submit event
 */
function handleSubmit(e) {
  e.preventDefault();
  const btn = e.target.querySelector('button[type="submit"]');
  btn.textContent = '✓ Message Sent!';
  btn.style.background = '#2A5640';
  setTimeout(() => {
    btn.textContent = 'Send Message';
    btn.style.background = '';
  }, 3000);
}