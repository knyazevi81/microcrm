// Import modules
import { setupSidebar } from './sidebar.js';
import { setupPages } from './pages.js';
import { initializeDealsPage, cleanupDealsPage } from './deals.js';

// Initialize the application when DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
  // Initialize sidebar functionality
  setupSidebar();
  
  // Initialize page switching functionality with cleanup handlers
  setupPages({
    initialPage: 'profile',
    onPageChange: (oldPage, newPage) => {
      // Cleanup handlers
      if (oldPage === 'deals') {
        cleanupDealsPage();
      }
      
      // Initialization handlers
      if (newPage === 'deals') {
        initializeDealsPage();
      }
    }
  });

  // Load initial page content
  initializeDealsPage();
  
  console.log('CRM panel initialized');
});