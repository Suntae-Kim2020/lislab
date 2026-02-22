(function() {
    'use strict';

    function init() {
        var groupsTo = document.getElementById('id_groups_to');
        var permsFrom = document.getElementById('id_user_permissions_from');
        var permsTo = document.getElementById('id_user_permissions_to');
        var staffCheckbox = document.getElementById('id_is_staff');
        var groupPermsMap = window.GROUP_PERMS_MAP || {};

        if (!groupsTo || !permsFrom || !permsTo) {
            return false;
        }
        if (Object.keys(groupPermsMap).length === 0) {
            return false;
        }

        var previousGroupIds = getAllOptionValues(groupsTo);

        var observer = new MutationObserver(function() {
            var currentGroupIds = getAllOptionValues(groupsTo);

            var added = currentGroupIds.filter(function(id) {
                return previousGroupIds.indexOf(id) === -1;
            });
            var removed = previousGroupIds.filter(function(id) {
                return currentGroupIds.indexOf(id) === -1;
            });

            added.forEach(function(gid) {
                var perms = groupPermsMap[gid] || [];
                perms.forEach(function(p) { movePerm(String(p.id), p.name, 'add'); });
            });

            removed.forEach(function(gid) {
                var perms = groupPermsMap[gid] || [];
                perms.forEach(function(p) { movePerm(String(p.id), p.name, 'remove'); });
            });

            if (staffCheckbox) {
                staffCheckbox.checked = currentGroupIds.length > 0;
            }

            previousGroupIds = currentGroupIds;

            try {
                if (typeof SelectFilter !== 'undefined') {
                    SelectFilter.refresh_icons('id_user_permissions');
                }
            } catch(e) {}
        });

        observer.observe(groupsTo, { childList: true });
        return true;

        function getAllOptionValues(sel) {
            var vals = [];
            for (var i = 0; i < sel.options.length; i++) {
                vals.push(sel.options[i].value);
            }
            return vals;
        }

        function movePerm(pid, pname, action) {
            if (action === 'add') {
                var fromOpt = permsFrom.querySelector('option[value="' + pid + '"]');
                if (fromOpt) permsFrom.removeChild(fromOpt);
                if (!permsTo.querySelector('option[value="' + pid + '"]')) {
                    permsTo.appendChild(new Option(pname, pid));
                }
            } else {
                var toOpt = permsTo.querySelector('option[value="' + pid + '"]');
                if (toOpt) permsTo.removeChild(toOpt);
                if (!permsFrom.querySelector('option[value="' + pid + '"]')) {
                    permsFrom.appendChild(new Option(pname, pid));
                }
            }
        }
    }

    // SelectFilter 위젯이 DOM을 변환한 뒤에 실행해야 함
    // load 이벤트 후에도 위젯이 없으면 폴링으로 대기
    function waitAndInit() {
        if (init()) return;
        var attempts = 0;
        var timer = setInterval(function() {
            attempts++;
            if (init() || attempts > 50) {
                clearInterval(timer);
            }
        }, 100);
    }

    if (document.readyState === 'complete') {
        waitAndInit();
    } else {
        window.addEventListener('load', waitAndInit);
    }
})();
