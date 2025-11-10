
document.addEventListener('DOMContentLoaded', function() {
    console.log('Coopel E-commerce cargado');
    
    function mostrarNotificacion(mensaje, tipo = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${tipo}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${mensaje}</span>
                <button class="notification-close">&times;</button>
            </div>
        `;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${tipo === 'success' ? '#48bb78' : '#e53e3e'};
            color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            z-index: 10000;
            max-width: 300px;
        `;
        
        document.body.appendChild(notification);
        
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => {
            notification.remove();
        });
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    function validarFormulario(form) {
        const inputs = form.querySelectorAll('input[required]');
        let valido = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.style.borderColor = '#e53e3e';
                valido = false;
            } else {
                input.style.borderColor = '#e2e8f0';
            }
        });
        
        return valido;
    }

    function formatearPrecio(precio) {
        return new Intl.NumberFormat('es-MX', {
            style: 'currency',
            currency: 'MXN'
        }).format(precio);
    }

    function manejarErrorImagen(img) {
        img.src = '/static/img/placeholder.jpg';
        img.alt = 'Imagen no disponible';
    }

    document.querySelectorAll('img').forEach(img => {
        img.addEventListener('error', function() {
            manejarErrorImagen(this);
        });
    });

    window.mostrarNotificacion = mostrarNotificacion;
    window.validarFormulario = validarFormulario;
    window.formatearPrecio = formatearPrecio;
    window.manejarErrorImagen = manejarErrorImagen;
});