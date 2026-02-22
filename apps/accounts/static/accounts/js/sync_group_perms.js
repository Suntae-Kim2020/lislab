(function() {
    'use strict';

    // DOM 로드 후 실행 (filter_horizontal 위젯이 초기화된 뒤)
    window.addEventListener('load', function() {
        var groupsTo = document.getElementById('id_groups_to');
        var permsFrom = document.getElementById('id_user_permissions_from');
        var permsTo = document.getElementById('id_user_permissions_to');
        var staffCheckbox = document.getElementById('id_is_staff');

        if (!groupsTo || !permsFrom || !permsTo) return;

        // 이전 그룹 상태 추적
        var previousGroupIds = getSelectedIds(groupsTo);

        // groups "to" 박스 변경 감시 (MutationObserver)
        var observer = new MutationObserver(function() {
            var currentGroupIds = getSelectedIds(groupsTo);

            // 추가된 그룹
            var added = currentGroupIds.filter(function(id) {
                return previousGroupIds.indexOf(id) === -1;
            });

            // 제거된 그룹
            var removed = previousGroupIds.filter(function(id) {
                return currentGroupIds.indexOf(id) === -1;
            });

            added.forEach(function(groupId) {
                fetchAndMovePermissions(groupId, 'add');
            });

            removed.forEach(function(groupId) {
                fetchAndMovePermissions(groupId, 'remove');
            });

            // 스태프 권한 자동 체크 (그룹이 하나라도 있으면)
            if (staffCheckbox) {
                staffCheckbox.checked = currentGroupIds.length > 0;
            }

            previousGroupIds = currentGroupIds;
        });

        observer.observe(groupsTo, { childList: true });

        function getSelectedIds(selectEl) {
            var ids = [];
            for (var i = 0; i < selectEl.options.length; i++) {
                ids.push(selectEl.options[i].value);
            }
            return ids;
        }

        function fetchAndMovePermissions(groupId, action) {
            // admin URL에서 그룹 권한 가져오기
            var url = window.location.pathname.replace(/\/change\/$/, '').replace(/\/\d+\//, '/') + 'group-permissions/' + groupId + '/';
            // URL 정리: /admin/accounts/user/group-permissions/{id}/
            var adminBase = window.location.pathname.match(/^(\/admin\/accounts\/user\/)/);
            if (adminBase) {
                url = adminBase[1] + 'group-permissions/' + groupId + '/';
            }

            var xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    var data = JSON.parse(xhr.responseText);
                    data.permissions.forEach(function(perm) {
                        movePermission(perm.id.toString(), perm.name, action);
                    });
                    // SelectFilter2 위젯 갱신
                    SelectFilter.refresh_icons('id_user_permissions');
                }
            };
            xhr.send();
        }

        function movePermission(permId, permName, action) {
            if (action === 'add') {
                // from → to 이동
                var fromOption = permsFrom.querySelector('option[value="' + permId + '"]');
                if (fromOption) {
                    permsFrom.removeChild(fromOption);
                    var newOption = document.createElement('option');
                    newOption.value = permId;
                    newOption.text = permName;
                    permsTo.appendChild(newOption);
                }
                // 이미 to에 있으면 스킵
            } else if (action === 'remove') {
                // to → from 이동
                var toOption = permsTo.querySelector('option[value="' + permId + '"]');
                if (toOption) {
                    permsTo.removeChild(toOption);
                    var newOpt = document.createElement('option');
                    newOpt.value = permId;
                    newOpt.text = permName;
                    permsFrom.appendChild(newOpt);
                }
            }
        }
    });
})();
