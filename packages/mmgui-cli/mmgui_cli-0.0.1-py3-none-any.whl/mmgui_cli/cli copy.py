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
    """MMGUI CLI: 快速创建桌面应用"""
    pass


@cli.command()
@click.argument("project_name")
def init(project_name):
    project_path = Path.cwd() / project_name
    project_module = project_name.lower()

    if project_path.exists():
        click.echo(f"❌ 错误：目录 {project_name} 已存在。")
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

    shutil.copytree(template_base, project_path)

    # 动态重命名 core_package -> project_module
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

    click.echo(f"✅ 成功创建项目 '{project_name}'，使用 '{selected_template}' 模板。")

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
        click.echo(f"> cd {project_name}")
        click.echo("> python -m venv .venv")
        click.echo("> source .venv/bin/activate    # Linux/macOS")
        click.echo("> .venv\\Scripts\\activate     # Windows")
        click.echo("> pip install mmgui")
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

    # 检查是否已存在 .venv（可选）
    venv_path = project_root / ".venv"
    if not venv_path.exists():
        click.echo("⚠️ 警告：未检测到虚拟环境（.venv），建议先创建。")

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

    # 执行命令
    try:
        subprocess.run(command, env=env, check=True, shell=shell)
    except subprocess.CalledProcessError as e:
        click.echo(
            f"❌ 启动失败：{e} 可能为当前终端、ide未激活正确的Python解释器，请使用 cmd 或 powershell 终端启动。",
        )


def replace_in_file(file_path: Path, old_str: str, new_str: str):
    """替换文件中的文本"""
    if not file_path.exists():
        return
    content = file_path.read_text(encoding="utf-8")
    content = content.replace(old_str, new_str)
    file_path.write_text(content, encoding="utf-8")
