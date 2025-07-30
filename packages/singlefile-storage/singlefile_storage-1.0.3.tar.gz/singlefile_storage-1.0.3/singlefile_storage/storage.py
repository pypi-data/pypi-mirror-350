#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: qicongsheng
import os
import sqlite3
from math import ceil

from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_httpauth import HTTPBasicAuth

users = {
    "admin": "password"
}
DATA_PATH = './data'
API_KEY = 'your-api-key'
app = Flask(__name__)
auth = HTTPBasicAuth()


def init_app():
    app.config.update({
        'UPLOAD_FOLDER': os.path.join(DATA_PATH, 'uploads'),  # 文件存储目录
        'DATABASE': os.path.join(DATA_PATH, 'storage.db'),  # SQLite数据库路径
        'MAX_CONTENT_LENGTH': 64 * 1024 * 1024,
        'ALLOWED_EXTENSIONS': {'html', 'htm'},
        'API_KEYS': {API_KEY},
        'ITEMS_PER_PAGE': 20  # 分页每页数量
    })
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with sqlite3.connect(app.config['DATABASE']) as conn:
        conn.execute('''
                     CREATE TABLE IF NOT EXISTS uploads
                     (
                         id
                         INTEGER
                         PRIMARY
                         KEY
                         AUTOINCREMENT,
                         filename
                         TEXT
                         NOT
                         NULL
                         UNIQUE,
                         original_url
                         TEXT
                         NOT
                         NULL,
                         uploaded_at
                         DATETIME
                         DEFAULT
                         CURRENT_TIMESTAMP
                     )
                     ''')


@auth.get_password
def get_password(username):
    if username in users:
        return users.get(username)
    return None


def get_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_name = filename
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], new_name)):
        new_name = f"{base}({counter}){ext}"
        counter += 1
    return new_name


LIST_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Manager</title>
    <style>
        :root {
            --primary: #2563eb;
            --danger: #dc2626;
            --gray-100: #f3f4f6;
            --gray-200: #e5e7eb;
            --gray-600: #4b5563;
            --white: #ffffff;
        }

        * {
            box-sizing: content-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', system-ui, sans-serif;
            background-color: var(--gray-100);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2rem;
        }

        .container {
            width: 100%;
            max-width: 1200px;
            background: var(--white);
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            padding: 2rem;
        }

        h1 {
            color: var(--primary);
            margin-bottom: 2rem;
            font-weight: 600;
            font-size: 1.875rem;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 1.5rem;
            table-layout: fixed;
        }

        th {
            background: var(--primary);
            color: var(--white);
            padding: 1rem;
            text-align: left;
            font-weight: 500;
            position: sticky;
            top: 0;
        }

        td {
            padding: 1rem;
            border-bottom: 1px solid var(--gray-200);
            color: var(--gray-600);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        tr:hover td {
            background-color: var(--gray-100);
        }

        /* 删除按钮样式 */
        .delete-btn {
            background: var(--danger);
            color: var(--white);
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 500;
        }

        .delete-btn:hover {
            background: #b91c1c;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(220, 38, 38, 0.2);
        }

        /* 分页样式 */
        .pagination {
            display: flex;
            gap: 0.5rem;
            justify-content: center;
            margin-top: 2rem;
        }

        .page-item {
            list-style: none;
        }

        .page-link {
            display: block;
            padding: 0.625rem 1.25rem;
            border-radius: 6px;
            background: var(--white);
            color: var(--primary);
            border: 1px solid var(--gray-200);
            text-decoration: none;
            transition: all 0.2s;
        }

        .page-link:hover {
            background: var(--primary);
            color: var(--white);
            border-color: var(--primary);
        }

        .current-page {
            background: var(--primary);
            color: var(--white);
            border-color: var(--primary);
        }

        .ellipsis {
            display: flex;
            align-items: center;
            padding: 0 1rem;
            color: var(--gray-600);
        }

        /* 响应式设计 */
        @media (max-width: 768px) {
            body {
                padding: 1rem;
            }

            .container {
                padding: 1rem;
            }

            th, td {
                padding: 0.75rem;
                font-size: 0.875rem;
            }

            .delete-btn {
                padding: 0.375rem 0.75rem;
                font-size: 0.875rem;
            }

            .page-link {
                padding: 0.5rem 1rem;
            }
        }

        .truncate {
            max-width: 0;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Managed Files</h1>
        
        <table>
            <thead>
                <tr>
                    <th style="width: 30%;">Filename</th>
                    <th style="width: 40%;">Original URL</th>
                    <th style="width: 15%;">Date</th>
                    <th style="width: 10%;">Size</th>
                    <th style="width: 5%;">Action</th>
                </tr>
            </thead>
            <tbody>
                {% for item in files %}
                <tr>
                    <td class="truncate">
                        <a href="/uploads/{{ item.filename }}">{{ item.filename }}</a>
                    </td>
                    <td class="truncate">
                        <a href="{{ item.original_url }}" target="_blank">{{ item.original_url }}</a>
                    </td>
                    <td>{{ item.uploaded_at }}</td>
                    <td>{{ (item.size // 1024)|abs }} KB</td>
                    <td>
                        <button class="delete-btn" onclick="deleteFile('{{ item.filename }}')">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                            </svg>
                        </button>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <div class="pagination">
            {% if pagination.has_prev %}
                <a class="page-link" href="{{ url_for('file_list', page=pagination.page-1) }}">&laquo;</a>
            {% endif %}
            
            {% set start_page = [1, pagination.page-2]|max %}
            {% set end_page = [pagination.total_pages, pagination.page+2]|min %}
            
            {% if start_page > 1 %}
                <a class="page-link" href="{{ url_for('file_list', page=1) }}">1</a>
                {% if start_page > 2 %}<span class="ellipsis">...</span>{% endif %}
            {% endif %}
            
            {% for p in range(start_page, end_page+1) %}
                {% if p == pagination.page %}
                    <span class="page-link current-page">{{ p }}</span>
                {% else %}
                    <a class="page-link" href="{{ url_for('file_list', page=p) }}">{{ p }}</a>
                {% endif %}
            {% endfor %}
            
            {% if end_page < pagination.total_pages %}
                {% if end_page < pagination.total_pages - 1 %}<span class="ellipsis">...</span>{% endif %}
                <a class="page-link" href="{{ url_for('file_list', page=pagination.total_pages) }}">
                    {{ pagination.total_pages }}
                </a>
            {% endif %}
            
            {% if pagination.has_next %}
                <a class="page-link" href="{{ url_for('file_list', page=pagination.page+1) }}">&raquo;</a>
            {% endif %}
        </div>
    </div>

    <script>
    function deleteFile(filename) {
                
        fetch(`/delete/${filename}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                alert('File deleted successfully');
                location.reload();
            } else {
                response.text().then(text => alert(`Delete failed: ${text}`));
            }
        })
        .catch(error => alert('Error: ' + error.message));
    }
    </script>
</body>
</html>"""


@app.route('/upload', methods=['POST'])
def upload_file():
    # Authentication
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Invalid Authorization header'}), 401
    token = auth_header.split(' ')[1]
    if token not in app.config['API_KEYS']:
        return jsonify({'error': 'Invalid API key'}), 403

    # File validation
    if 'singlehtmlfile' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['singlehtmlfile']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not ('.' in file.filename and
            file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']):
        return jsonify({'error': 'Invalid file type'}), 400

    # URL validation
    url = request.form.get('url', '').strip()
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    # Save file
    filename = get_unique_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        file.save(save_path)
        # Database operation
        with sqlite3.connect(app.config['DATABASE']) as conn:
            conn.execute('''
                         INSERT INTO uploads (filename, original_url)
                         VALUES (?, ?)
                         ''', (filename, url))
    except Exception as e:
        if os.path.exists(save_path):
            os.remove(save_path)
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'message': 'File uploaded successfully',
        'filename': filename,
        'original_url': url
    }), 200


@app.route('/delete/<filename>', methods=['DELETE', 'GET'])
@auth.login_required
def delete_file(filename):
    # Delete from database
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cur = conn.execute('DELETE FROM uploads WHERE filename = ?', (filename,))
        if cur.rowcount == 0:
            return jsonify({'error': 'File not found'}), 404

    # Delete local file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            return jsonify({'error': f'File deletion failed: {str(e)}'}), 500

    return jsonify({'message': 'File deleted successfully'}), 200


@app.route('/list')
@auth.login_required
def file_list():
    page = request.args.get('page', 1, type=int)
    per_page = app.config['ITEMS_PER_PAGE']

    with sqlite3.connect(app.config['DATABASE']) as conn:
        conn.row_factory = sqlite3.Row

        # Get total count
        total = conn.execute('SELECT COUNT(*) FROM uploads').fetchone()[0]
        total_pages = ceil(total / per_page) if total else 1

        # Validate page number
        page = max(1, min(page, total_pages))
        offset = (page - 1) * per_page

        # Get paginated data
        cur = conn.execute('''
                           SELECT filename,
                                  original_url,
                                  datetime(uploaded_at) as uploaded_at
                           FROM uploads
                           ORDER BY uploaded_at DESC LIMIT ?
                           OFFSET ?
                           ''', (per_page, offset))
        files = cur.fetchall()

    # Get file sizes
    files_with_size = []
    for item in files:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], item['filename'])
        size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        files_with_size.append({
            'filename': item['filename'],
            'original_url': item['original_url'],
            'uploaded_at': item['uploaded_at'],
            'size': size
        })

    return render_template_string(LIST_TEMPLATE,
                                  files=files_with_size,
                                  pagination={
                                      'page': page,
                                      'total_pages': total_pages,
                                      'has_prev': page > 1,
                                      'has_next': page < total_pages
                                  })


@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def start(port=5000):
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    start()
