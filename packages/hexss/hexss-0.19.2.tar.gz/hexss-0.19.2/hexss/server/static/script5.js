class ContextMenu {
    constructor(menuSelector) {
        this.menuElement = document.querySelector(menuSelector);
        this.menuItems = {
            'Download': { action: () => this.downloadItem() },
            'Rename': { action: () => this.renameItem() },
            'Delete': { action: () => this.deleteItem() },
            'Edit': {
                condition: (path) => this.isTextFile(path),
                action: () => this.editFile()
            },
            'Extract': {
                condition: (path) => this.isZipFile(path),
                action: () => this.extractFile(),
                subMenu: {
                    'Extract': { action: () => this.extractFile() },
                    'Extract Here': { action: () => this.extractHere() }
                }
            }
        };
    }

    show(x, y, target) {
        this.selectedItem = target;
        this.updateMenuItems(target.dataset.path);
        this.menuElement.style.left = `${x}px`;
        this.menuElement.style.top = `${y}px`;
        this.menuElement.style.display = 'block';
    }

    hide() {
        this.menuElement.style.display = 'none';
    }

     updateMenuItems(path) {
        const menuList = this.menuElement.querySelector('ul');
        menuList.innerHTML = '';

        Object.keys(this.menuItems).forEach((key) => {
            const menuItemConfig = this.menuItems[key];

            if (!menuItemConfig.condition || menuItemConfig.condition(path)) {
                const menuItem = document.createElement('li');
                menuItem.textContent = key;

                if (menuItemConfig.subMenu) {
                    const subMenu = document.createElement('ul');
                    subMenu.classList.add('submenu');

                    Object.keys(menuItemConfig.subMenu).forEach((subKey) => {
                        const subMenuItemConfig = menuItemConfig.subMenu[subKey];
                        const subMenuItem = document.createElement('li');
                        subMenuItem.textContent = subKey;
                        subMenuItem.onclick = subMenuItemConfig.action;
                        subMenu.appendChild(subMenuItem);
                    });

                    menuItem.appendChild(subMenu);
                }
                else {
                    menuItem.onclick = menuItemConfig.action;
                }
                menuList.appendChild(menuItem);
            }
        });
    }

    isTextFile(path) {
        return /\.(txt|md|js|py|html|css|json|xml|csv|log|gitignore)$/i.test(path);
    }

    isZipFile(path) {
        return path.endsWith('.zip');
    }

    // Action handlers
    downloadItem() {
        const path = this.selectedItem.dataset.path;
        window.location.href = `/download?path=${encodeURIComponent(path)}`;
    }

    renameItem() {
        const oldPath = this.selectedItem.dataset.path;
        const newName = prompt('Enter new name:');
        if (newName) {
            const newPath = oldPath.substring(0, oldPath.lastIndexOf('/') + 1) + newName;
            $.post('/rename', { old_path: oldPath, new_path: newPath })
                .done(() => location.reload())
                .fail(err => alert(`Failed to rename item: ${err.statusText}`));
        }
    }

    deleteItem() {
        const path = this.selectedItem.dataset.path;
        if (confirm('Are you sure you want to delete this item?')) {
            $.post('/delete', { path })
                .done(() => location.reload())
                .fail(err => alert(`Failed to delete item: ${err.statusText}`));
        }
    }

    editFile() {
        const path = this.selectedItem.dataset.path;
        $.get(`/edit?path=${encodeURIComponent(path)}`)
            .done((data) => {
                if (data.success) {
                    $('#file-name').val(path.split('/').pop());
                    $('#edit-content').val(data.content);
                    $('#edit-modal').show();
                } else {
                    alert('Failed to load file content');
                }
            })
            .fail(err => alert(`Failed to load file: ${err.statusText}`));
    }

    extractFile() {
        const path = this.selectedItem.dataset.path;
        const folderName = prompt('Enter folder name for extraction:');
        if (folderName) {
            $.post('/extract_file', { path, folder_name: folderName })
                .done((data) => {
                    if (data.success) {
                        // alert('File extracted successfully');
                        location.reload();
                    } else {
                        alert(`Failed to extract file: ${data.error}`);
                    }
                })
                .fail(err => alert(`Failed to extract file: ${err.statusText}`));
        }
    }

    extractHere() {
        const path = this.selectedItem.dataset.path;
        $.post('/extract_file', { path, folder_name: '' })
            .done(() => {
                // alert('File extracted successfully here');
                location.reload();
            })
            .fail(err => alert(`Failed to extract file here: ${err.statusText}`));
    }
}

class TextFile {
    constructor() {
        this.isNew = false;
        this.selectedItem = null;
    }

    create() {
        this.isNew = true;
        $('#file-name').val('');
        $('#edit-content').val('');
        $('#edit-modal').show();
    }

    edit(target) {
        this.isNew = false;
        this.selectedItem = target;
        const path = target.dataset.path;
        const fileName = path.split('/').pop();

        $('#file-name').val(fileName);

        $.get(`/edit?path=${encodeURIComponent(path)}`)
            .done((data) => {
                if (data.success) {
                    $('#edit-content').val(data.content);
                    $('#edit-modal').show();
                } else {
                    alert('Failed to load file content');
                }
            })
            .fail((jqXHR, textStatus, errorThrown) => {
                alert(`Failed to load file: ${errorThrown}`);
            });
    }

    save(currentPathInputSelector = '#upload-form input[name="current_path"]') {
        const fileName = $('#file-name').val();
        const content = $('#edit-content').val();
        let path;

        if (this.isNew) {
            path = ($(currentPathInputSelector).val() + '/' + fileName).replace(/\\/g, '/');
        } else {
            const oldPath = this.selectedItem.dataset.path;
            const directory = oldPath.substring(0, oldPath.lastIndexOf('/') + 1);
            path = (directory + fileName).replace(/\\/g, '/');
        }

        $.post(`/edit?path=${encodeURIComponent(path)}`, { content: content })
            .done((data) => {
                if (data.success) {
                    $('#edit-modal').hide();
                    alert('File saved successfully');
                    location.reload();
                } else {
                    alert('Failed to save file');
                }
            })
            .fail((jqXHR, textStatus, errorThrown) => {
                alert(`Failed to save file: ${errorThrown}`);
            });
    }

    cancelEdit() {
        $('#edit-modal').hide();
    }

    delete(target) {
        const path = target.dataset.path;

        if (confirm('Are you sure you want to delete this file?')) {
            $.post('/delete', { path })
                .done(() => location.reload())
                .fail((err) => alert(`Failed to delete file: ${err.statusText}`));
        }
    }
}



const contextMenu = new ContextMenu('#context-menu');
const textFile = new TextFile();

function handleContextMenu(event, contextMenuSelector) {
    event.preventDefault();
    const target = event.target.closest('a');
    if (target) {
        contextMenu.show(event.pageX, event.pageY, target);
    } else {
        contextMenu.hide();
    }
}

function createFolder() {
    const folderName = prompt('Enter folder name:');
    if (folderName) {
        const path = ($('#upload-form input[name="current_path"]').val() + '/' + folderName).replace(/\\/g, '/');
        $.post('/create_folder', {path: path})
            .done(function (data) {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Failed to create folder');
                }
            })
            .fail(function (jqXHR, textStatus, errorThrown) {
                alert(`Failed to create folder: ${errorThrown}`);
            });
    }
}




document.querySelector('#file-list').addEventListener('contextmenu', (e) => handleContextMenu(e));
document.querySelector('#directory-list').addEventListener('contextmenu', (e) => handleContextMenu(e));

document.addEventListener('click', (event) => {
    contextMenu.hide();
});

document.getElementById("create-folder-btn").onclick = function() {createFolder()};
document.getElementById("create-file-btn").onclick = function() {
    const textFile = new TextFile();

};

$(document).ready(function () {

    // Prevent default behavior for file drag and drop
    $(document).on('drag dragstart dragend dragover dragenter dragleave drop', function (e) {
        e.preventDefault();
        e.stopPropagation();
    });

    // Handle file drop
    $(document).on('drop', function (e) {
        let droppedFiles = e.originalEvent.dataTransfer.files;
        $('#file-upload').prop('files', droppedFiles);
        $('#upload-form').submit();
    });
});