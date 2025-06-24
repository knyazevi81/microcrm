/**
 * Sets up the sidebar functionality
 */
export function setupSidebar() {
    const body = document.body;
    const toggleBtn = document.getElementById('toggle-sidebar');
    const closeSidebarBtn = document.getElementById('close-sidebar');
    const overlay = document.getElementById('overlay');

    // Function to toggle sidebar
    const toggleSidebar = () => {
        body.classList.toggle('sidebar-open');
        if (body.classList.contains('sidebar-open')) {
            body.classList.remove('sidebar-was-closed-manually');
        } else {
            body.classList.add('sidebar-was-closed-manually');
        }
    };

    // Event listeners
    toggleBtn.addEventListener('click', toggleSidebar);

    if (closeSidebarBtn) {
        closeSidebarBtn.addEventListener('click', () => {
            body.classList.remove('sidebar-open');
            body.classList.add('sidebar-was-closed-manually');
        });
    }

    if (overlay) {
        overlay.addEventListener('click', () => {
            body.classList.remove('sidebar-open');
            body.classList.add('sidebar-was-closed-manually');
        });
    }

    // Handle window resize event to manage sidebar state
    window.addEventListener('resize', () => {
        if (window.innerWidth >= 992) {
            // For desktop, sidebar should be open by default
            if (!body.classList.contains('sidebar-was-closed-manually')) {
                 body.classList.add('sidebar-open');
            }
        } else {
            // For mobile, sidebar should be closed by default
            body.classList.remove('sidebar-open');
            body.classList.remove('sidebar-was-closed-manually');
        }
    });

    // Initialize sidebar state based on screen size
    if (window.innerWidth >= 992) {
        body.classList.add('sidebar-open');
    }
}