document.addEventListener('DOMContentLoaded', function () {
  // Mobile sidebar toggle
  var hamburger = document.getElementById('hamburger');
  var sidebar = document.getElementById('sidebar');
  if (hamburger && sidebar) {
    hamburger.addEventListener('click', function () {
      sidebar.classList.toggle('open');
    });
  }

  // Attendance toggle visual state
  document.querySelectorAll('.att-toggle input').forEach(function (input) {
    var syncLabel = function () {
      var wrapper = input.closest('.att-toggle');
      if (!wrapper) return;
      wrapper.querySelectorAll('label').forEach(function (lbl) {
        lbl.classList.remove('is-checked');
      });
      if (input.checked) {
        input.closest('label').classList.add('is-checked');
      }
    };
    input.addEventListener('change', syncLabel);
    syncLabel();
  });

  // Auto-hide toast messages
  document.querySelectorAll('.toast').forEach(function (toast, i) {
    setTimeout(function () {
      toast.style.transition = 'opacity 0.5s ease';
      toast.style.opacity = '0';
      setTimeout(function () { toast.remove(); }, 500);
    }, 4000 + i * 300);
  });

  // Animate stat numbers counting up
  document.querySelectorAll('.stat-value[data-count]').forEach(function (el) {
    var target = parseFloat(el.getAttribute('data-count')) || 0;
    var suffix = el.getAttribute('data-suffix') || '';
    var current = 0;
    var steps = 30;
    var increment = target / steps;
    var count = setInterval(function () {
      current += increment;
      if (current >= target) {
        current = target;
        clearInterval(count);
      }
      el.textContent = (Number.isInteger(target) ? Math.round(current) : current.toFixed(1)) + suffix;
    }, 25);
  });
});
