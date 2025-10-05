from pathlib import Path
import textwrap

path = Path('routes/backend.py')
text = path.read_text(encoding='utf-8')
old = "@backend_bp.route('/users')\r\ndef users():\r\n    \"\"\"?�戶管�?\"\"\"\r\n    users = User.query.all()\r\n    return render_template('backend/users.html', users=users)\r\n\r\n\r\n"
if old not in text:
    raise SystemExit('old block not found')

new = textwrap.dedent("""\
@backend_bp.route('/users')
def users():
    \"\"\"用戶管理\"\"\"
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('backend/users.html', users=users)


@backend_bp.route('/users/create', methods=['GET', 'POST'])
def create_user():
    \"\"\"新增用戶\"\"\"
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        is_admin = bool(request.form.get('is_admin'))
        is_active = bool(request.form.get('is_active'))

        if not name or not email or not password:
            flash('請填寫必填欄位', 'error')
            return render_template('backend/create_user.html', form_data=request.form)

        if User.query.filter_by(email=email).first():
            flash('電子信箱已存在', 'error')
            return render_template('backend/create_user.html', form_data=request.form)

        user = User(
            name=name,
            email=email,
            phone=phone,
            is_admin=is_admin,
            is_active=is_active
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('用戶建立成功', 'success')
        return redirect(url_for('backend.users'))

    return render_template('backend/create_user.html')


@backend_bp.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    \"\"\"刪除用戶\"\"\"
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash('無法刪除當前登入的帳號', 'error')
        return redirect(url_for('backend.users'))

    if user.is_admin:
        flash('無法刪除管理員帳號', 'error')
        return redirect(url_for('backend.users'))

    db.session.delete(user)
    db.session.commit()

    flash('用戶已刪除', 'success')
    return redirect(url_for('backend.users'))


""")

text = text.replace(old, new)
path.write_text(text, encoding='utf-8')
