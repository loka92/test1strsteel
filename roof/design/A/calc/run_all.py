"""Re-runs the complete Alternative A calculation chain.  python3 run_all.py"""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
for script in ('frame2d.py', 'sections.py', 'frames_model.py', 'checks_members.py', 'checks_secondary.py',
               'checks_connections.py', 'report_build.py', 'report_assemble.py', 'pynite_check.py'):
    print('\n' + '=' * 30, script, '=' * 30)
    r = subprocess.run([sys.executable, os.path.join(HERE, script)], capture_output=True, text=True)
    print(r.stdout[-6000:] if script != 'report_build.py' else r.stdout[-800:])
    if r.returncode:
        print(r.stderr); sys.exit(1)
print('\nALL DONE')
