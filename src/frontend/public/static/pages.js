/**
 * Sets up page switching functionality
 */
export function setupPages({ onPageChange, initialPage = 'dashboard' } = {}) {
    const navItems = document.querySelectorAll('.sidebar-nav li');
    const pages = document.querySelectorAll('.page');
    const pageTitle = document.getElementById('page-title');
    const body = document.body;
    
    let currentPage = initialPage;
    
    // Function to switch to a specific page
    const switchToPage = (pageName) => {
      const oldPage = currentPage;
      currentPage = pageName;
      
      // Update navigation items
      navItems.forEach(item => {
        if (item.dataset.page === pageName) {
          item.classList.add('active');
        } else {
          item.classList.remove('active');
        }
      });
      
      // Update pages
      pages.forEach(page => {
        if (page.id === `${pageName}-page`) {
          page.classList.add('active');
        } else {
          page.classList.remove('active');
        }
      });
      
      // Update page title
      if (pageTitle) {
        const pageNavItem = document.querySelector(`.sidebar-nav li[data-page="${pageName}"] .nav-text`);
        pageTitle.textContent = pageNavItem ? pageNavItem.textContent : pageName.charAt(0).toUpperCase() + pageName.slice(1);
      }
      
      // On mobile, close the sidebar after selecting a page
      if (window.innerWidth < 992) {
        body.classList.remove('sidebar-open');
      }
      
      // Call the page change handler if provided
      if (onPageChange) {
        onPageChange(oldPage, pageName);
      }
    };
    
    // Add click event listeners to navigation items
    navItems.forEach(item => {
      item.addEventListener('click', () => {
        const pageName = item.dataset.page;
        switchToPage(pageName);
      });
    });

    // Set initial page
    switchToPage(currentPage);
  }