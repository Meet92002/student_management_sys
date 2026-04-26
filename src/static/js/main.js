const showLoader = () => {
    const loader = document.getElementById('loader-overlay');
    if (loader) loader.classList.add('active');
};
const hideLoader = () => {
    const loader = document.getElementById('loader-overlay');
    if (loader) loader.classList.remove('active');
};

let currentPage = 1;
const limit = 8;
let allStudentCache = []; 
let searchQuery = '';

async function loadStudents() {
    const table = document.getElementById('students-table');
    const studentCountEl = document.getElementById('student-count');
    
    if (!table && !studentCountEl) return; 

    showLoader();
    try {
        const res = await fetch(`/api/students?page=${currentPage}&limit=${limit}&search=${encodeURIComponent(searchQuery)}`);
        const responseData = await res.json();

        if (studentCountEl) studentCountEl.textContent = responseData.total;
        
        const pageInfoEl = document.getElementById('page-info');
        if (pageInfoEl) pageInfoEl.textContent = `Page ${currentPage}`;

        // Load Prof count too
        const profRes = await fetch('/api/staff/count');
        const profData = await profRes.json();
        const profEl = document.getElementById('prof-count');
        if(profEl) profEl.textContent = profData.total;

        allStudentCache = responseData.data; 

        renderTable(allStudentCache);

        // Handle pagination buttons
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        
        if (prevBtn) prevBtn.disabled = currentPage === 1;
        
        const totalPages = Math.ceil(responseData.total / limit);
        if (nextBtn) nextBtn.disabled = currentPage >= totalPages || totalPages === 0;

    } catch (e) {
        console.error("Failed to load students", e);
    } finally {
        hideLoader();
    }
}

function renderTable(students) {
    const tbody = document.querySelector('#students-table tbody');
    if (!tbody) return;
    
    tbody.innerHTML = '';

    if (students.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; color: var(--text-secondary);">No records found.</td></tr>`;
        return;
    }

    students.forEach(student => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><input type="checkbox" class="student-cb" value="${student.student_id}"></td>
            <td>${student.name}</td>
            <td>${student.email}</td>
            <td>${student.age}</td>
            <td>${student.enrollment_date}</td>
            <td style="display:flex; gap: 0.5rem;">
                <button onclick="window.location.href='/student/${student.student_id}'" class="btn" style="background:#3b82f6; color:white;">
                    Profile
                </button>
                <button onclick="openEditModal('${student.student_id}')" class="btn">
                    Edit
                </button>
                <button onclick="deleteStudent('${student.student_id}')" class="btn btn-danger">
                    Delete
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    const selectAllCb = document.getElementById('select-all-cb');
    if(selectAllCb) selectAllCb.checked = false;
    updateBulkDeleteBtnVisibility();
}

function updateBulkDeleteBtnVisibility() {
    const checked = document.querySelectorAll('.student-cb:checked');
    const bulkBtn = document.getElementById('bulk-delete-btn');
    if (bulkBtn) {
        bulkBtn.style.display = checked.length > 0 ? 'inline-block' : 'none';
    }
}

// Attach listeners for bulk selection
document.querySelector('#students-table')?.addEventListener('change', (e) => {
    if (e.target.id === 'select-all-cb') {
        const cbs = document.querySelectorAll('.student-cb');
        cbs.forEach(cb => cb.checked = e.target.checked);
        updateBulkDeleteBtnVisibility();
    } else if (e.target.classList.contains('student-cb')) {
        const allCbs = document.querySelectorAll('.student-cb');
        const checkedCbs = document.querySelectorAll('.student-cb:checked');
        const selectAllCb = document.getElementById('select-all-cb');
        if (selectAllCb) {
            selectAllCb.checked = allCbs.length === checkedCbs.length;
        }
        updateBulkDeleteBtnVisibility();
    }
});

// Student Search Logic for System Records
let searchTimeout;
const studentSearchInput = document.getElementById('search-input');
const studentClearBtn = document.getElementById('clear-records-search');

if (studentSearchInput && studentClearBtn) {
    studentSearchInput.addEventListener('input', (e) => {
        // Toggle clear button
        studentClearBtn.style.display = e.target.value ? 'block' : 'none';

        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            searchQuery = e.target.value;
            currentPage = 1; // Reset to first page on search
            loadStudents();
        }, 400); // Debounce search
    });

    studentClearBtn.addEventListener('click', () => {
        studentSearchInput.value = '';
        studentClearBtn.style.display = 'none';
        searchQuery = '';
        currentPage = 1;
        loadStudents();
        studentSearchInput.focus();
    });
}

// Modal Logic
const modal = document.getElementById('add-modal');
document.getElementById('add-student-btn')?.addEventListener('click', () => modal.classList.add('active'));
document.getElementById('close-modal')?.addEventListener('click', () => modal.classList.remove('active'));

// Form Submit POST
document.getElementById('add-student-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoader();

    const newStudent = {
        name: document.getElementById('form-name').value,
        email: document.getElementById('form-email').value,
        age: parseInt(document.getElementById('form-age').value),
        enrollment_date: new Date().toISOString().split('T')[0]
    };

    try {
        await fetch('/api/students', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newStudent)
        });
        modal.classList.remove('active');
        document.getElementById('add-student-form').reset();
        currentPage = 1; 
    } catch (e) {
        console.error(e);
    } finally {
        hideLoader();
        loadStudents();
    }
});

const editModal = document.getElementById('edit-modal');
document.getElementById('close-edit-modal')?.addEventListener('click', () => editModal.classList.remove('active'));

function openEditModal(id) {
    const student = allStudentCache.find(s => s.student_id === id);
    if (!student) return;
    document.getElementById('edit-form-id').value = student.student_id;
    document.getElementById('edit-form-name').value = student.name;
    document.getElementById('edit-form-email').value = student.email;
    document.getElementById('edit-form-age').value = student.age;
    editModal.classList.add('active');
}

document.getElementById('edit-student-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoader();

    const id = document.getElementById('edit-form-id').value;
    const updatedStudent = {
        name: document.getElementById('edit-form-name').value,
        email: document.getElementById('edit-form-email').value,
        age: parseInt(document.getElementById('edit-form-age').value)
    };

    try {
        await fetch(`/api/students/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedStudent)
        });
        editModal.classList.remove('active');
        document.getElementById('edit-student-form').reset();
    } catch (e) {
        console.error(e);
    } finally {
        hideLoader();
        loadStudents();
    }
});

document.getElementById('prev-btn')?.addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        loadStudents();
    }
});
document.getElementById('next-btn')?.addEventListener('click', () => {
    currentPage++;
    loadStudents();
});

async function deleteStudent(id) {
    if (!confirm("Are you sure you want to delete this student record?")) return;
    showLoader();
    try {
        await fetch(`/api/students/${id}`, { method: 'DELETE' });
    } catch (e) {
        console.error(e);
    } finally {
        hideLoader();
        loadStudents();
    }
}

document.getElementById('bulk-delete-btn')?.addEventListener('click', async () => {
    const checked = document.querySelectorAll('.student-cb:checked');
    if (checked.length === 0) return;
    
    if (!confirm(`Are you sure you want to delete ${checked.length} selected records?`)) return;
    
    const ids = Array.from(checked).map(cb => cb.value);
    
    showLoader();
    try {
        await fetch('/api/students/bulk-delete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ student_ids: ids })
        });
    } catch (e) {
        console.error(e);
    } finally {
        hideLoader();
        loadStudents();
    }
});

document.getElementById('import-btn')?.addEventListener('click', async () => {
    showLoader();
    try {
        await fetch('/api/import-dummy', { method: 'POST' });
        currentPage = 1;
    } catch (e) {
        console.error(e);
    } finally {
        hideLoader();
        loadStudents();
    }
});

document.getElementById('export-csv-btn')?.addEventListener('click', () => {
    window.location.href = '/api/export/csv';
});


async function loadLatestNotice() {
    try {
        const res = await fetch('/api/notices');
        const notices = await res.json();
        if (notices.length > 0) {
            const latest = notices[0];
            const ticker = document.getElementById('notice-ticker');
            const tickerText = document.getElementById('ticker-text');
            if (ticker && tickerText) {
                const author = latest.posted_by ? ` [Posted by ${latest.posted_by}]` : '';
                tickerText.textContent = `${latest.title}: ${latest.content}${author}`;
                ticker.style.display = 'flex';
            }
        }
    } catch(e) {
        // fail silently
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadStudents();
    loadLatestNotice();

    // Global Search Implementation
    const globalSearchInput = document.getElementById('global-search');
    const searchResults = document.getElementById('search-results');

    if (globalSearchInput && searchResults) {
        const globalClearBtn = document.getElementById('clear-global-search');

        globalSearchInput.addEventListener('input', async (e) => {
            const query = e.target.value.trim();
            
            // Toggle clear button
            if (globalClearBtn) {
                globalClearBtn.style.display = query ? 'block' : 'none';
            }

            if (query.length < 2) {
                searchResults.style.display = 'none';
                return;
            }
            try {
                const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
                const data = await res.json();

                if (data.length > 0) {
                    searchResults.innerHTML = data.map(item => `
                        <div class="search-item" style="padding: 1rem; border-bottom: 1px solid var(--border-color); cursor: pointer; transition: background 0.2s;" onclick="window.location.href='${item.url}'">
                            <div style="font-weight: 600; color: var(--text-primary);">${item.name}</div>
                            <div style="font-size: 0.8rem; color: var(--text-secondary); text-transform: uppercase;">${item.type}</div>
                        </div>
                    `).join('');
                    searchResults.style.display = 'block';
                } else {
                    searchResults.innerHTML = '<div style="padding: 1rem; color: var(--text-secondary); text-align: center;">No results found.</div>';
                    searchResults.style.display = 'block';
                }
            } catch (err) {
                console.error("Search failed", err);
            }
        });

        // Close search results when clicking outside
        document.addEventListener('click', (e) => {
            if (!globalSearchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });

        if (globalClearBtn) {
            globalClearBtn.addEventListener('click', () => {
                globalSearchInput.value = '';
                globalClearBtn.style.display = 'none';
                searchResults.style.display = 'none';
                globalSearchInput.focus();
            });
        }

        // Add hover effect style dynamically
        const style = document.createElement('style');
        style.textContent = `
            .search-item:hover {
                background: var(--bg-color);
            }
        `;
        document.head.appendChild(style);
    }
});
