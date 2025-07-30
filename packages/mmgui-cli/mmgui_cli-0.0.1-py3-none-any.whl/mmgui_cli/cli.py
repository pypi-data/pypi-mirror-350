from pathlib import Path
import os
import shutil
import click
import inquirer
import subprocess
import stat
import sys


TEMPLATE_DIR = Path(__file__).parent / "templates"


@click.group()
def cli():
    """MMGUI CLI: 快速创建mmgui桌面应用"""
    pass


@cli.command()
@click.argument("project_name", required=False)
def init(project_name):
    """初始化项目结构（在当前目录中生成）"""
    project_path = Path.cwd()
    if project_name:
        project_name = project_name
    else:
        project_name = project_path.name
    project_module = project_name.lower()

    # 检查当前目录是否为空
    if any(project_path.iterdir()):
        confirm = click.confirm(f"⚠️ 当前目录 {project_name} 不为空。是否继续初始化？")
        if not confirm:
            click.echo("❌ 操作取消。")
            return

    # 获取可用模板
    templates = [d.name for d in TEMPLATE_DIR.iterdir() if d.is_dir()]
    questions = [
        inquirer.List(
            "template",
            message="请选择前端模板",
            choices=templates,
        ),
        inquirer.List(
            "auto_script",
            message="是否生成一键安装脚本",
            choices=["是", "否"],
        ),
    ]
    answers = inquirer.prompt(questions)
    if not answers:
        click.echo("❌ 操作取消。")
        return

    selected_template = answers["template"]
    auto_generate_script = answers["auto_script"] == "是"

    # 创建项目结构
    template_base = Path(__file__).parent / "templates" / "base"
    template_frontend = Path(__file__).parent / "templates" / selected_template

    # 复制基础模板到当前目录
    for item in template_base.iterdir():
        dest = project_path / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    # 重命名 core_package -> project_module
    old_core_dir = project_path / "core_package"
    new_core_dir = project_path / project_module

    if old_core_dir.exists():
        old_core_dir.rename(new_core_dir)
    else:
        click.echo(f"⚠️ 警告：未找到 core_package 目录，请检查模板结构。")

    # 替换 functions.py 中的导入路径
    functions_py_path = project_path / "gui" / "functions.py"
    replace_in_file(
        functions_py_path, "from core_package.core", f"from {project_module}.core"
    )

    # 替换 index.html（如果模板不是 base）
    if selected_template != "base":
        gui_ui_dir = project_path / "gui" / "ui"
        gui_ui_dir.mkdir(exist_ok=True)
        shutil.copy(template_frontend / "index.html", gui_ui_dir / "index.html")

    # 生成 README.md
    readme_template = template_base / "README.md.tpl"
    if readme_template.exists():
        context = {"project_name": project_name, "project_module": project_module}
        readme_content = render_template(
            readme_template.read_text(encoding="utf-8"), context
        )
        (project_path / "README.md").write_text(readme_content, encoding="utf-8")
    # 删除生成后的README.md.tpl
    generated_readme = project_path / "README.md.tpl"
    if generated_readme.exists():
        generated_readme.unlink()

    # 删除生成后的脚本
    generated_script_sh = project_path / "scripts" / "setup_dev.sh.tpl"
    generated_script_bat = project_path / "scripts" / "setup_dev.bat.tpl"
    if generated_script_sh.exists() and generated_script_bat.exists():
        generated_script_sh.unlink()
        generated_script_bat.unlink()

    click.echo(
        f"✅ 成功在当前目录 '{project_name}' 初始化项目，使用 '{selected_template}' 模板。"
    )

    # 生成一键安装脚本（可选）
    if auto_generate_script:
        script_dir = project_path / "scripts"
        script_dir.mkdir(exist_ok=True)

        sh_script = script_dir / "setup_dev.sh"
        bat_script = script_dir / "setup_dev.bat"

        # 读取模板并写入
        sh_script.write_text(
            (
                Path(__file__).parent
                / "templates"
                / "base"
                / "scripts"
                / "setup_dev.sh.tpl"
            ).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        bat_script.write_text(
            (
                Path(__file__).parent
                / "templates"
                / "base"
                / "scripts"
                / "setup_dev.bat.tpl"
            ).read_text(encoding="utf-8"),
            encoding="utf-8",
        )

        # 设置执行权限（Linux/macOS）
        st = os.stat(sh_script)
        os.chmod(sh_script, st.st_mode | stat.S_IEXEC)

        click.echo("✨ 已生成并正在运行一键安装脚本...")

        # 自动运行脚本
        try:
            if os.name == "nt":  # Windows
                subprocess.run(
                    [str(bat_script)], shell=True, check=True, cwd=project_path
                )
            else:  # Linux / macOS
                subprocess.run(["./setup_dev.sh"], check=True, cwd=script_dir)
        except subprocess.CalledProcessError as e:
            click.echo(f"❌ 脚本运行失败：{e}")
    else:
        click.echo("👉 接下来请运行以下命令启动项目：\n")
        click.echo("> pip install -r requirements.txt\n")
        click.echo("> python -m gui.app\n")


@cli.command()
def run():
    """启动桌面应用（自动激活虚拟环境）"""
    project_root = Path.cwd()

    # 检查 gui/app.py 是否存在
    app_path = project_root / "gui" / "app.py"
    if not app_path.exists():
        click.echo("❌ 错误：未找到 gui/app.py，你可能不在项目根目录。")
        return

    # 获取项目模块名（与当前目录名一致）
    project_module = project_root.name.lower()

    # 检查模块是否存在
    module_dir = project_root / project_module
    if not module_dir.exists():
        click.echo(
            f"❌ 错误：未找到模块目录 {project_module}/，请确认项目已正确初始化。"
        )
        return

    venv_path = project_root / ".venv"
    env = os.environ.copy()

    if venv_path.exists():
        click.echo("✔ 已激活虚拟环境")

        if os.name == "nt":  # Windows
            activate_script = venv_path / "Scripts" / "activate.bat"
            command = [str(activate_script), "&&", sys.executable, "-m", "gui.app"]
            shell = True
        else:  # Linux / macOS
            activate_script = venv_path / "bin" / "activate"
            command = [
                "/bin/bash",
                "-c",
                f"source {activate_script} && python -m gui.app",
            ]
            shell = False

    else:
        click.echo("⚠️ 未找到虚拟环境（.venv），将使用当前 Python 环境运行...")
        command = [sys.executable, "-m", "gui.app"]
        shell = False

    # 设置 PYTHONPATH 到项目根目录，以便导入模块
    env["PYTHONPATH"] = str(project_root)

    # 执行命令
    try:
        subprocess.run(command, env=env, check=True, shell=shell)
    except subprocess.CalledProcessError as e:
        click.echo(
            f"❌ 启动失败：{e}。可能是终端或IDE未激活正确的Python解释器，请尝试使用 cmd 或 powershell 启动。",
        )


def replace_in_file(file_path: Path, old_str: str, new_str: str):
    """替换文件中的文本"""
    if not file_path.exists():
        return
    content = file_path.read_text(encoding="utf-8")
    content = content.replace(old_str, new_str)
    file_path.write_text(content, encoding="utf-8")


def render_template(content: str, context: dict) -> str:
    """简单模板渲染：将内容中的 {{ variable }} 替换为上下文中的值"""
    for key, value in context.items():
        placeholder = f"{{{{ {key} }}}}"
        content = content.replace(placeholder, str(value))
    return content
