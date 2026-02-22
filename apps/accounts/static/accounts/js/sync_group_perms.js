(function() {
    'use strict';

    function init() {
        var groupsTo = document.getElementById('id_groups_to');
        var permsFrom = document.getElementById('id_user_permissions_from');
        var permsTo = document.getElementById('id_user_permissions_to');
        var staffCheckbox = document.getElementById('id_is_staff');

        if (!groupsTo || !permsFrom || !permsTo) {
            console.log('[sync_group_perms] 위젯을 찾을 수 없습니다.');
            return;
        }

        console.log('[sync_group_perms] 초기화 완료');

        // API URL: /admin/accounts/user/group-permissions/{id}/
        var apiBase = '/admin/accounts/user/group-permissions/';

        // 이전 그룹 상태
        var previousGroupIds = getAllOptionValues(groupsTo);
        console.log('[sync_group_perms] 초기 그룹:', previousGroupIds);

        // groups "to" 박스 변경 감시
        var observer = new MutationObserver(function() {
            var currentGroupIds = getAllOptionValues(groupsTo);

            var added = currentGroupIds.filter(function(id) {
                return previousGroupIds.indexOf(id) === -1;
            });
            var removed = previousGroupIds.filter(function(id) {
                return currentGroupIds.indexOf(id) === -1;
            });

            console.log('[sync_group_perms] 변경 감지 - added:', added, 'removed:', removed);

            added.forEach(function(gid) { syncPermissions(gid, 'add'); });
            removed.forEach(function(gid) { syncPermissions(gid, 'remove'); });

            // 스태프 권한 자동 체크
            if (staffCheckbox) {
                staffCheckbox.checked = currentGroupIds.length > 0;
            }

            previousGroupIds = currentGroupIds;
        });

        observer.observe(groupsTo, { childList: true });

        function getAllOptionValues(sel) {
            var vals = [];
            for (var i = 0; i < sel.options.length; i++) {
                vals.push(sel.options[i].value);
            }
            return vals;
        }

        function syncPermissions(groupId, action) {
            var url = apiBase + groupId + '/';
            console.log('[sync_group_perms] fetch:', url, action);

            fetch(url, {
                credentials: 'same-origin',
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(function(resp) { return resp.json(); })
            .then(function(data) {
                console.log('[sync_group_perms] 응답:', data.permissions.length, '개 권한');
                data.permissions.forEach(function(perm) {
                    var pid = String(perm.id);
                    if (action === 'add') {
                        // from → to
                        var opt = permsFrom.querySelector('option[value="' + pid + '"]');
                        if (opt) {
                            permsFrom.removeChild(opt);
                        }
                        // to에 없으면 추가
                        if (!permsTo.querySelector('option[value="' + pid + '"]')) {
                            var newOpt = new Option(perm.name, pid);
                            permsTo.appendChild(newOpt);
                        }
                    } else {
                        // to → from
                        var opt2 = permsTo.querySelector('option[value="' + pid + '"]');
                        if (opt2) {
                            permsTo.removeChild(opt2);
                        }
                        if (!permsFrom.querySelector('option[value="' + pid + '"]')) {
                            var newOpt2 = new Option(perm.name, pid);
                            permsFrom.appendChild(newOpt2);
                        }
                    }
                });

                // Django SelectFilter 위젯 갱신
                try {
                    if (typeof SelectFilter !== 'undefined') {
                        SelectFilter.refresh_icons('id_user_permissions');
                    }
                } catch(e) {
                    console.log('[sync_group_perms] refresh_icons 에러 (무시):', e);
                }
            })
            .catch(function(err) {
                console.error('[sync_group_perms] fetch 에러:', err);
            });
        }
    }

    // filter_horizontal 위젯이 초기화된 뒤 실행
    if (document.readyState === 'complete') {
        init();
    } else {
        window.addEventListener('load', init);
    }
})();
