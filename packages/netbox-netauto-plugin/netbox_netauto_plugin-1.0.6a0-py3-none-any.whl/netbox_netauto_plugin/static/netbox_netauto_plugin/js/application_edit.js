function redirectToLink() {
    var sys_id = document.getElementById('id_ritm').value;
    if (sys_id) {
        var url = 'https://kbcacc.service-now.com/sc_task.do?sys_id=' + sys_id;
        window.open(url, '_blank');
    } else {
        alert('Please select a value for RITM.');
    }
}

// Obecná funkce pro přepínání stavů tlačítek a divů
function toggleButtonState(buttonToDeactivate, buttonToActivate, divId) {
    // Deaktivace aktuálního tlačítka
    buttonToDeactivate.classList.remove('active');
    buttonToDeactivate.tabIndex = -1;
    buttonToDeactivate.setAttribute('aria-selected', 'false');

    // Aktivace tlačítka
    if (buttonToActivate) {
        buttonToActivate.classList.add('active');
        buttonToActivate.setAttribute('aria-selected', 'true');
        buttonToActivate.tabIndex = 0;

        const targetDiv = document.getElementById(buttonToActivate.id.slice(0, -4)); // Odstranění posledních 4 znaků z ID - _tab
        if (targetDiv) {
            targetDiv.classList.add('active', 'show');
        }
    }

    // Skrytí divu spojeného s původním tlačítkem - jednotlive polozky pod tabem, maji stejne ID ovsem na konci Id neni "_tab"
    if (divId) {
        const targetDiv = document.getElementById(divId);
        if (targetDiv) {
            targetDiv.classList.remove('active', 'show');
        }
    }
}

// Obecná funkce pro zpracování chování tlačítek
function handleButtonBehavior(button, liElements, toggleTo) {
    const targetButton = Array.from(liElements).find(li => {
        const b = li.querySelector('button');
        return b && b.textContent.trim() === toggleTo;
    })?.querySelector('button');

    const divId = button.id ? button.id.slice(0, -4) : null;
    toggleButtonState(button, targetButton, divId);
}

// Metoda pro zpracování tlačítek
function handleButtonActions(button, objectName, liElements) {
    const buttonText = button.textContent.trim();
    var skip_dialog = false;
    switch (objectName) {
        case "Client SSL Profile":
            if (buttonText === "Existing") {
                // console.log("Checking if Custom is filled");
                const ssl_cert = document.getElementById("id_client_ssl_certificate").value;
                const ssl_srv_name = document.getElementById("id_client_ssl_server_name").value;
                if (!ssl_cert && !ssl_srv_name) {
                    // console.log("Custom is empty - continue");
                    skip_dialog = true;
                }
            } else if (buttonText === "Custom") {
                const monitor_profile = document.querySelector('div > select#id_client_ssl_profile').parentNode.querySelector('.ts-control div[data-ts-item]');
                // console.log(monitor_profile);
                if (!monitor_profile) {
                    // console.log("Monitor profile is empty - continue");
                    skip_dialog = true;
                }
            }
            break;
        case "Health Monitor":
            if (buttonText === "Existing") {
                // console.log("Checking if Custom is filled");
                const send_string = document.getElementById("id_send_string").value;
                const receive_string = document.getElementById("id_receive_string").value;
                if (!send_string && !receive_string) {
                    // console.log("Custom is empty - continue");
                    skip_dialog = true;
                }
            } else if (buttonText === "Custom") {
                const monitor_profile = document.querySelector('div > select#id_health_monitor_profile').parentNode.querySelector('.ts-control div[data-ts-item]');
                // console.log(monitor_profile);
                if (!monitor_profile) {
                    // console.log("Monitor profile is empty - continue");
                    skip_dialog = true;
                }
            }
            break;
    }

    const confirmAction = skip_dialog || confirm(
        `Jste si jisti, že chcete pokračovat s tlačítkem "${buttonText}" v objektu "${objectName}"?`
    );

    if (!confirmAction) {
        if (objectName === "Client SSL Profile" && buttonText === "Existing") {
            handleButtonBehavior(button, liElements, "Custom");
        } else if (objectName === "Client SSL Profile" && buttonText === "Custom") {
            handleButtonBehavior(button, liElements, "Existing");
        } else if (objectName === "Health Monitor" && buttonText === "Existing") {
            handleButtonBehavior(button, liElements, "Custom");
        } else if (objectName === "Health Monitor" && buttonText === "Custom") {
            handleButtonBehavior(button, liElements, "Existing");
        }
    } else {
        switch (objectName) {
            case "Client SSL Profile":
                if (buttonText === "Existing") {
                    // console.log("Client SSL Profile - Resetting Custom fields");
                    document.getElementById("id_client_ssl_certificate").value = "";
                    document.getElementById("id_client_ssl_cert_authority").value = "";
                    document.getElementById("id_client_ssl_profile-ts-label").classList.add('required');
                    document.getElementById("id_client_ssl_auth_mode-ts-label").classList.remove('required');
                    document.querySelector('label[for=id_client_ssl_certificate]').classList.remove('required');
                    document.getElementById("id_client_ssl_certificate").required = false;
                } else if (buttonText === "Custom") {
                    // console.log("Client SSL Profile - Resetting Existing fields");
                    document.querySelector('div > select#id_client_ssl_profile').parentNode.querySelector('.ts-control i').click()
                    document.getElementById("id_client_ssl_profile-ts-label").classList.remove('required');
                    document.getElementById("id_client_ssl_auth_mode-ts-label").classList.add('required');
                    document.querySelector('label[for=id_client_ssl_certificate]').classList.add('required');
                    document.getElementById("id_client_ssl_certificate").required = true;
                }
                break;
            case "Health Monitor":
                if (buttonText === "Existing") {
                    // console.log("Health Monitor - Resetting Custom fields");
                    document.getElementById("id_send_string").value = "";
                    document.getElementById("id_receive_string").value = "";
                    document.getElementById("id_interval").value = 5;
                    document.getElementById("id_timeout").value = 16;
                    document.getElementById("id_health_monitor_profile-ts-label").classList.add('required');
                    document.getElementById("id_send_string").required = false;
                    document.getElementById("id_receive_string").required = false;
                    document.querySelector('label[for=id_send_string]').classList.remove('required');
                    document.querySelector('label[for=id_receive_string]').classList.remove('required');
                } else if (buttonText === "Custom") {
                    // console.log("Health Monitor - Resetting Existing fields");
                    document.querySelector('div > select#id_health_monitor_profile').parentNode.querySelector('.ts-control i').click()
                    document.getElementById("id_health_monitor_profile-ts-label").classList.remove('required');
                    document.getElementById("id_send_string").required = true;
                    document.getElementById("id_receive_string").required = true;
                    document.querySelector('label[for=id_send_string]').classList.add('required');
                    document.querySelector('label[for=id_receive_string]').classList.add('required');
                }
                break;
        }
    }
}

function netbox_app_init() {
    // Najde všechny divy s class "field-group mb-5"
    const fieldGroups = document.querySelectorAll('.field-group.mb-5');
    const result = [];

    // Zpracování divů a tlačítek
    fieldGroups.forEach(div => {
        const h2Element = div.querySelector('h2');
        const ulElement = div.querySelector('ul.nav.nav-pills.mb-1');

        if (ulElement) {
            const liElements = ulElement.querySelectorAll('li');
            const validButtons = Array.from(liElements).filter(li => {
                const button = li.querySelector('button');
                return button && (button.textContent.trim() === "Custom" || button.textContent.trim() === "Existing");
            });

            if (liElements.length === 2 && validButtons.length === 2 && h2Element) {
                const objectName = h2Element.textContent.trim();

                const buttonsList = validButtons.map(li => {
                    const button = li.querySelector('button');

                    if (button && button.id) {
                        button.addEventListener('click', () => {
                            handleButtonActions(button, objectName, liElements);
                        });
                    }

                    return {
                        id: button.id || null, // Pokud button nemá id, nastaví null
                        name: button.textContent.trim()
                    };
                });

                result.push({
                    name: objectName,
                    buttons: buttonsList
                });
            }
        }
    });

    // vypis objektu s id a name tlacitky vcetne sekce
    // console.log(result);
}

document.addEventListener("DOMContentLoaded", function(event) {
    netbox_app_init();
});
