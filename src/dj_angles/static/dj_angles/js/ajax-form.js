/**
 * A custom element which enhances a form so it submits via AJAX and replaces itself.
 * 
 * Based on https://gomakethings.com/progressively-enhancing-forms-with-an-html-web-component-part-2/ with a few tweaks.
 */
class AjaxForm extends HTMLElement {
  constructor() {
    super()

    // Define options
    this.delay = this.hasAttribute('delay') ? this.attributes['delay'].value : 0
    
    // TODO: Support other swap values from https://htmx.org/attributes/hx-swap/
    this.swap = this.hasAttribute('swap') ? this.attributes['swap'].value : "outerHTML"

    if (!['outerHTML', 'innerHTML'].includes(this.swap)) {
      throw new Error(`Invalid swap value: ${this.swap}`)
    }
  }

  connectedCallback() {
    this.form = this.querySelector('form');

    if (!this.form) {
      throw new Error('Form element not found')
    }

    // Set up event listeners and other initialization logic
    this.form.addEventListener('submit', this)
  }

  /**
   * Handle events on the component.
   * @param  {Event} event The event object
   */
  handleEvent(event) {
    this[`on${event.type}`](event)
  }

  /**
   * Handle submit events.
   * @param {Event} event The event object
   */
  async onsubmit(event) {
    // Stop form from reloading the page
    event.preventDefault()

    // If the form is already submitting, do nothing
    // Otherwise, disable future submissions
    if (this.isDisabled()) {
      return
    }

    this.disable()

    try {
      // Call the API via fetch
      const { action, method } = this.form
      const formData = this.serialize(event)

      const response = await fetch(action, {
        method,
        body: formData,
        headers: {
          'Content-type': 'application/x-www-form-urlencoded',
          'X-Requested-With': 'XMLHttpRequest'
        }
      })

      // If there's an error, raise it
      if (!response.ok) {
        throw new Error(response.statusText)
      }

      // Get the replacement HTML from the response
      if (["outerHTML", "innerHTML"].includes(this.swap)) {
        this[this.swap] = await response.text()
      }

      // Emit custom event
      this.emit(formData)
    } catch (error) {
      console.warn(error)
    } finally {
      setTimeout(() => {
        this.enable()
      }, this.delay)
    }
  }

  /**
   * Disable the form so it can't be submitted while waiting for the API.
   */
  disable() {
    this.setAttribute('form-submitting', '')
  }

  /**
   * Enable the form after the API returns.
   */
  enable() {
    this.removeAttribute('form-submitting')
  }

  /**
   * Check if a form is submitting to the API.
   * @return {Boolean} If true, the form is submitting.
   */
  isDisabled() {
    return this.hasAttribute('form-submitting')
  }

  /**
   * Serialize all form data into an encoded query string.
   * @param {Event} event The event that triggered the submission.
   * @return {String} The serialized form data
   */
  serialize(event) {
    let data = new FormData(this.form)
    let params = new URLSearchParams()

    for (let [key, val] of data) {
      params.append(key, val)
    }

    // Add the submitter's name and value, i.e. the button that was clicked
    params.append(event.submitter.name, event.submitter.value)

    return params.toString()
  }

  /**
   * Emit a custom event.
   * @param {Object} detail Any details to pass along with the event.
   */
  emit(detail = {}) {
    // Create a new event
    const event = new CustomEvent('ajax-form', {
      bubbles: true,
      cancelable: false,
      detail: detail
    })

    // Dispatch the event
    return this.dispatchEvent(event)
  }
}

// Only register `ajax-form` custom element if it has not been registered already
if (!customElements.get('ajax-form')) {
  customElements.define('ajax-form', AjaxForm)
}
