import Sortable from 'sortablejs';

const DEALS_API_ENDPOINT = '/deals/list';
const dealStatuses = [
    { id: 'new', title: 'Новые' },
    { id: 'in-progress', title: 'В работе' },
    { id: 'client-wait', title: 'Ожидание клиента' },
];

let sortableInstances = [];
let actionBar;
let deleteZone;
let closeZone;
let draggedItem = null;

// --- Mock API Fetch ---
// In a real application, this would be a network request.
// We are mocking it to simulate the backend call to "/deals/list".
async function fetchDeals() {
    console.log(`Fetching deals from ${DEALS_API_ENDPOINT}...`);
    // Mock data as the backend is not available
    const mockDeals = [
        { telegram_id: 12345, first_name: 'Иван', username: 'ivan_p', phone_number: '+79111234567', status: 'new' },
        { telegram_id: 67890, first_name: 'Мария', username: 'maria_k', phone_number: '+79219876543', status: 'new' },
        { telegram_id: 54321, first_name: 'Петр', username: 'petr_s', phone_number: '+79055554433', status: 'in-progress' },
        { telegram_id: 98765, first_name: 'Анна', username: 'anna_m', phone_number: '+79998887766', status: 'in-progress' },
        { telegram_id: 11223, first_name: 'Сергей', username: 'sergey_v', phone_number: '+79161112233', status: 'client-wait' },
    ];
    
    return new Promise(resolve => {
        setTimeout(() => {
            console.log("Deals fetched successfully (mocked).");
            resolve(mockDeals);
        }, 500);
    });
}


function createKanbanCard(deal) {
    const card = document.createElement('div');
    card.className = 'kanban-card';
    card.dataset.id = deal.telegram_id;
    card.innerHTML = `
        <div class="kanban-card-title">${deal.first_name}</div>
        <div class="kanban-card-company">@${deal.username || 'N/A'}</div>
        <div class="kanban-card-footer">
            <span class="kanban-card-phone">${deal.phone_number}</span>
        </div>
    `;
    return card;
}

function updateColumnCount(columnElement) {
    const count = columnElement.querySelectorAll('.kanban-card').length;
    const countElement = columnElement.querySelector('.kanban-column-count');
    if(countElement) {
        countElement.textContent = count;
    }
}

function handleDragOver(e) {
    e.preventDefault();
    if(e.target.closest('.kanban-action-zone.delete')) {
        deleteZone.classList.add('hover');
    } else {
        deleteZone.classList.remove('hover');
    }

    if(e.target.closest('.kanban-action-zone.close')) {
        closeZone.classList.add('hover');
    } else {
        closeZone.classList.remove('hover');
    }
}

function handleDrop(e) {
    e.preventDefault();
    if (!draggedItem) return;

    if (e.target.closest('.kanban-action-zone.delete')) {
        const dealId = draggedItem.dataset.id;
        console.log(`Deal ${dealId} dropped on DELETE`);
        draggedItem.remove();
        // Here you would call an API to delete the deal
    } else if (e.target.closest('.kanban-action-zone.close')) {
        const dealId = draggedItem.dataset.id;
        console.log(`Deal ${dealId} dropped on CLOSE`);
        draggedItem.remove();
        // Here you would call an API to close the deal
    }

    // This will be called on drop, so we need to update column count
    // if it was dropped on an action zone
    const fromColumnEl = document.querySelector('.sortable-ghost').parentElement.closest('.kanban-column');
    if (fromColumnEl) {
        // A small delay to ensure DOM is updated after sortablejs logic
        setTimeout(() => updateColumnCount(fromColumnEl), 0);
    }
}

function renderKanbanBoard(deals) {
    const board = document.getElementById('kanban-board');
    if (!board) return;

    actionBar = document.getElementById('kanban-action-bar');
    deleteZone = document.getElementById('kanban-action-delete');
    closeZone = document.getElementById('kanban-action-close');

    board.innerHTML = '';
    sortableInstances.forEach(instance => instance.destroy());
    sortableInstances = [];

    dealStatuses.forEach(status => {
        const column = document.createElement('div');
        column.className = 'kanban-column';
        column.dataset.status = status.id;
        column.innerHTML = `
            <div class="kanban-column-header">
                <h4 class="kanban-column-title">${status.title}</h4>
                <span class="kanban-column-count">0</span>
            </div>
            <div class="kanban-cards"></div>
        `;
        board.appendChild(column);

        const cardsContainer = column.querySelector('.kanban-cards');
        const dealsInColumn = deals.filter(deal => deal.status === status.id);

        dealsInColumn.forEach(deal => {
            cardsContainer.appendChild(createKanbanCard(deal));
        });

        updateColumnCount(column);
        
        const sortable = new Sortable(cardsContainer, {
            group: 'deals',
            animation: 150,
            ghostClass: 'sortable-ghost',
            onStart: (evt) => {
                draggedItem = evt.item;
                actionBar.classList.add('visible');
            },
            onEnd: (evt) => {
                const itemEl = evt.item;
                const toColumnEl = evt.to.closest('.kanban-column');
                const fromColumnEl = evt.from.closest('.kanban-column');
                
                if (toColumnEl && fromColumnEl) {
                     // Update status on backend (mocked)
                    const dealId = itemEl.dataset.id;
                    const newStatus = toColumnEl.dataset.status;
                    console.log(`Deal ${dealId} moved to ${newStatus}`);

                    // Update column counts
                    updateColumnCount(fromColumnEl);
                    if (fromColumnEl !== toColumnEl) {
                        updateColumnCount(toColumnEl);
                    }
                }
               
                draggedItem = null;
                actionBar.classList.remove('visible');
                deleteZone.classList.remove('hover');
                closeZone.classList.remove('hover');
            }
        });
        sortableInstances.push(sortable);
    });

    if (actionBar) {
        actionBar.addEventListener('dragover', handleDragOver);
        actionBar.addEventListener('drop', handleDrop);
    }
}

export async function initializeDealsPage() {
    try {
        const deals = await fetchDeals();
        renderKanbanBoard(deals);
    } catch (error) {
        console.error('Failed to initialize deals page:', error);
        const board = document.getElementById('kanban-board');
        if (board) {
            board.innerHTML = '<p class="error-message">Не удалось загрузить сделки.</p>';
        }
    }
}

export function cleanupDealsPage() {
    sortableInstances.forEach(instance => instance.destroy());
    sortableInstances = [];
    if (actionBar) {
        actionBar.removeEventListener('dragover', handleDragOver);
        actionBar.removeEventListener('drop', handleDrop);
    }
    console.log('Deals page cleaned up.');
}