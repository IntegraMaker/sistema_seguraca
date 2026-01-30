(() => {
    'use strict'
  
    const getStoredTheme = () => localStorage.getItem('theme')
    const setStoredTheme = theme => localStorage.setItem('theme', theme)
  
    const getPreferredTheme = () => {
      const storedTheme = getStoredTheme()
      if (storedTheme) {
        return storedTheme
      }
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    }
  
    const setTheme = theme => {
      if (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.setAttribute('data-bs-theme', 'dark')
      } else {
        document.documentElement.setAttribute('data-bs-theme', theme)
      }
    }
  
    setTheme(getPreferredTheme())
  
    const showActiveTheme = (theme) => {
      const btnToActive = document.querySelector('#bd-theme')
      const icon = btnToActive.querySelector('i')
  
      if (!btnToActive) return

      btnToActive.className = 'btn btn-link nav-link px-0 px-lg-2'
      
      if (theme === 'dark') {
          icon.className = 'bi bi-moon-stars-fill fs-5'
      } else {
          icon.className = 'bi bi-sun-fill fs-5'
      }
    }
  
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      const storedTheme = getStoredTheme()
      if (storedTheme !== 'light' && storedTheme !== 'dark') {
        setTheme(getPreferredTheme())
      }
    })
  
    window.addEventListener('DOMContentLoaded', () => {
      showActiveTheme(getPreferredTheme())
  
      document.querySelectorAll('#bd-theme').forEach(toggle => {
        toggle.addEventListener('click', () => {
          const currentTheme = document.documentElement.getAttribute('data-bs-theme')
          const theme = currentTheme === 'dark' ? 'light' : 'dark'
          
          setStoredTheme(theme)
          setTheme(theme)
          showActiveTheme(theme)
        })
      })
    })
  })()