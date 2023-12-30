const toggleSwitch = document.querySelector('#dark-mode-toggle');

function setTheme(theme) {
    const themeStyle = document.querySelector('#theme-style');
    themeStyle.href = '/static/css/' + theme;

    localStorage.setItem('preferredTheme', theme);
}

function handleToggleChange() {
    if (toggleSwitch.checked) {
        setTheme('dark.css');
    } else {
        setTheme('light.css');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    toggleSwitch.addEventListener('change', handleToggleChange);
})

if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    toggleSwitch.checked = true;
    setTheme('dark.css');
} else {
    const storedTheme = localStorage.getItem('preferredTheme');
    if (storedTheme) {
        toggleSwitch.checked = storedTheme === 'dark.css';
        setTheme(storedTheme);
    }
}
