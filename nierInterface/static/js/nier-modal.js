/**
 * @Author: Jahleel Lacascade <jahleel>
 * @Date:   2020-10-22T18:40:28-04:00
 * @Email:  vabyz971@gmail.com
 * @Last modified by:   jahleel
 * @Last modified time: 2020-10-22T22:08:52-04:00
 * @License: GPLv3
 */

let modal = null
const focusSelector = "button, a, input, textarea"
let focusables = []

const openModal = async function(e) {
  e.preventDefault()
  const target = e.target.getAttribute('data-target')
  if (target.startsWith('#')) {
    modal = document.querySelector(target)
  } else {
    modal = await loadModal(target)
  }
  focusables = Array.from(modal.querySelectorAll(focusSelector))
  modal.style.display = null
  modal.removeAttribute('aria-hidden')
  modal.setAttribute('aria-modal', 'true')
  modal.addEventListener('click', closeModal)
  modal.querySelector('.js-modal-close').addEventListener('click', closeModal)
  modal.querySelector('.js-modal-stop').addEventListener('click', stopPropagation)
}

const closeModal = function(e) {
  if (modal === null) return
  e.preventDefault()
  modal.setAttribute('aria-hidden', 'true')
  modal.removeAttribute('aria-modal')
  modal.removeEventListener('click', closeModal)
  modal.querySelector('.js-modal-close').removeEventListener('click', closeModal)
  modal.querySelector('.js-modal-stop').removeEventListener('click', stopPropagation)
  window.setTimeout(function() {
    modal.style.display = "none"
    modal = null
  }, 400)
}

const loadModal = async function(url) {
  const target = '#' + url.split('#')[1]
  const html = await fetch(url).then(response => response.text())
  const element = document.createRange().createContextualFragment(html).querySelector(target)
  if (element == null) throw `Modal non trouver`
  document.body.append(element)
  return element
}


const stopPropagation = function(e) {
  e.stopPropagation()
}

const focusInModal = function(e) {
  e.preventDefault()
  let index = focusables.findIndex(f => f === modal.querySelector(':focus'))
  if (e.shiftKey == true) {
    index--
  } else {
    index++
  }
  if (index >= focusables.length) {
    index = 0
  }
  if (index < 0) {
    index = focusables.length - 1
  }
  focusables[index].focus()
}

document.querySelectorAll("a[data-toggle]").forEach(a => {
  a.addEventListener('click', openModal)

});

window.addEventListener('keydown', function(e) {
  if (e.key === "Escape" || e.key === "Esc") {
    closeModal(e)
  }
  if (e.key === 'Tab' && modal !== null) {
    focusInModal(e)
  }
})