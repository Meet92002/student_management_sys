const showLoader = () => document.getElementById('loader-overlay').classList.add('active');
const hideLoader = () => document.getElementById('loader-overlay').classList.remove('active');

let currentPage = 1;
const limit = 8;
let allStudentCache = []; // We'll cache all data on frontend for instant search buffering if needed, or search over the returned paginated context. Let's do backend pagination with frontend local filtering for simplicity.

async function loadStudents() {
    showLoader();
    try {
        const res = await fetch(`/api/students?page=${currentPage}&limit=${limit}`);
        const responseData = await res.json();

        document.getElementById('student-count').textContent = responseData.total;
        document.getElementById('page-info').textContent = `Page ${currentPage}`;

        // Load Prof count too
        const profRes = await fetch('/api/staff/count');
        const profData = await profRes.json();
        const profEl = document.getElementById('prof-count');
        if(profEl) profEl.textContent = profData.total;

        allStudentCache = responseData.data; // The current page data

        renderTable(allStudentCache);

        // Handle pagination buttons
        document.getElementById('prev-btn').disabled = currentPage === 1;
        const totalPages = Math.ceil(responseData.total / limit);
        document.getElementById('next-btn').disabled = currentPage >= totalPages || totalPages === 0;

        await loadChart(); // Re-render chart based on latest data
    } catch (e) {
        console.error("Failed to load students", e);
    } finally {
        hideLoader();
    }
}

function renderTable(students) {
    const tbody = document.querySelector('#students-table tbody');
    tbody.innerHTML = '';

    if (students.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; color: var(--text-secondary);">No records found.</td></tr>`;
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

    // Reset select all checkbox
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

// Search Logic
document.getElementById('search-input')?.addEventListener('keyup', (e) => {
    const query = e.target.value.toLowerCase();
    // Filter the cached view on current page 
    const filtered = allStudentCache.filter(student =>
        student.name.toLowerCase().includes(query) || student.email.toLowerCase().includes(query)
    );
    renderTable(filtered);
});

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
        currentPage = 1; // Return to page 1 to see the new entry
    } catch (e) {
        console.error(e);
    } finally {
        hideLoader();
        loadStudents();
    }
});

// Edit Modal Logic
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

// Edit Form Submit PUT
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

// Pagination Listenters
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

// Delete and Import Action overrides
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

// Chart.js Logic
let chartInstance = null;
async function loadChart() {
    try {
        const res = await fetch('/api/reports/subjects');
        const data = await res.json();

        const ctx = document.getElementById('gradesChart');
        if (!ctx) return;

        if (data.length === 0) {
            // No data to chart
            return;
        }

        const labels = data.map(d => d.subject);
        const averages = data.map(d => d.average);

        // Chart.js Global defaults for dark mode
        Chart.defaults.color = '#94a3b8';
        Chart.defaults.font.family = "'Inter', sans-serif";

        if (chartInstance) {
            chartInstance.destroy();
        }

        chartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Subject Averages',
                    data: averages,
                    backgroundColor: 'rgba(59, 130, 246, 0.8)',
                    borderColor: '#3b82f6',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: { color: 'rgba(51, 65, 85, 0.5)' }
                    },
                    x: {
                        grid: { display: false }
                    }
                }
            }
        });

    } catch (e) {
        console.error("Failed to load chart data", e);
    }
}

let attendanceChartInstance = null;
async function loadAttendanceChart() {
    try {
        const res = await fetch('/api/reports/attendance');
        const data = await res.json();
        const ctx = document.getElementById('attendanceChart');
        if (!ctx) return;

        if (data.length === 0) return;

        const labels = data.map(d => d.name);
        // data.attendance_rate is out of 100
        const rates = data.map(d => d.attendance_rate);

        Chart.defaults.color = '#94a3b8';
        Chart.defaults.font.family = "'Inter', sans-serif";

        if (attendanceChartInstance) {
            attendanceChartInstance.destroy();
        }

        attendanceChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Attendance Rate (%)',
                    data: rates,
                    backgroundColor: 'rgba(16, 185, 129, 0.8)',
                    borderColor: '#10b981',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: { color: 'rgba(51, 65, 85, 0.5)' }
                    },
                    x: {
                        grid: { display: false }
                    }
                }
            }
        });
    } catch (e) {
        console.error("Failed to load attendance chart", e);
    }
}

document.getElementById('refresh-chart-btn')?.addEventListener('click', async () => {
    showLoader();
    try {
        await fetch('/api/maintenance/cleanup', { method: 'POST' });
        await loadChart();
        await loadAttendanceChart();
    } catch (e) {
        console.error(e);
    } finally {
        hideLoader();
    }
});

// Initial Load
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
        // fail silently if not on dashboard
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadStudents();
    loadAttendanceChart();
    loadLatestNotice();
});
