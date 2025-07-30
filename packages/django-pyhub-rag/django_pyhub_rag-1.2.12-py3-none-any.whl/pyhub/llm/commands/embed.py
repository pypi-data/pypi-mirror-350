import logging
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from pyhub import init
from pyhub.llm import LLM
from pyhub.llm.json import json_dumps, json_loads, JSONDecodeError
from pyhub.llm.types import LLMEmbeddingModelEnum, Usage

app = typer.Typer(name="embed", help="LLM 임베딩 관련 명령")
console = Console()


@app.command()
def fill_jsonl(
    jsonl_path: Path = typer.Argument(..., help="소스 JSONL 파일 경로"),
    jsonl_out_path: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="출력 JSONL 파일 경로 (디폴트: 입력 jsonl 파일 경로에 -out 을 추가한 경로를 사용합니다.)",
    ),
    embedding_model: LLMEmbeddingModelEnum = typer.Option(
        LLMEmbeddingModelEnum.TEXT_EMBEDDING_3_SMALL,
        "--embedding-model",
        "-m",
        help="임베딩 모델",
    ),
    toml_path: Optional[Path] = typer.Option(
        Path.home() / ".pyhub.toml",
        "--toml-file",
        help="toml 설정 파일 경로 (디폴트: ~/.pyhub.toml)",
    ),
    env_path: Optional[Path] = typer.Option(
        Path.home() / ".pyhub.env",
        "--env-file",
        help="환경 변수 파일(.env) 경로 (디폴트: ~/.pyhub.env)",
    ),
    is_force: bool = typer.Option(False, "--force", "-f", help="확인 없이 출력 폴더 삭제 후 재생성"),
    is_verbose: bool = typer.Option(False, "--verbose", help="상세한 처리 정보 표시"),
):
    """JSONL 파일 데이터의 page_content 필드 값을 임베딩하고 embedding 필드에 저장합니다."""

    if jsonl_path.suffix.lower() != ".jsonl":
        console.print(f"[red]{jsonl_path} 파일이 jsonl 확장자가 아닙니다.[/red]")
        raise typer.Exit(1)

    # 출력 경로가 지정되지 않은 경우 기존 자동 생성 로직 사용
    if jsonl_out_path is None:
        jsonl_out_path = jsonl_path.with_name(f"{jsonl_path.stem}-out{jsonl_path.suffix}")

    if jsonl_out_path.exists() and not is_force:
        console.print(f"[red]오류: 출력 파일 {jsonl_out_path}이(가) 이미 존재합니다. 진행할 수 없습니다.[/red]")
        raise typer.Exit(1)

    if is_verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    init(debug=True, log_level=log_level, toml_path=toml_path, env_path=env_path)

    llm = LLM.create(embedding_model)

    if is_verbose:
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("설정", style="cyan")
        table.add_column("값", style="green")
        table.add_row("임베딩된 jsonl 파일 생성 경로", str(jsonl_out_path))
        table.add_row("임베딩 모델", f"{llm.embedding_model} ({llm.get_embed_size()})")
        table.add_row("toml 파일 경로", str(toml_path))
        table.add_row("환경변수 파일 경로", str(env_path))
        console.print(table)

    console.print(f"{jsonl_path} ...")
    total_usage = Usage()

    try:
        with jsonl_out_path.open("wt", encoding="utf-8") as out_f:
            with jsonl_path.open("rt", encoding="utf-8") as in_f:
                lines = tuple(in_f)
                total_lines = len(lines)

                for i, line in enumerate(lines):
                    obj = json_loads(line.strip())

                    # Skip if page_content field doesn't exist
                    if "page_content" not in obj:
                        continue

                    # Create embedding field if it doesn't exist
                    embedding = obj.get("embedding")
                    if not embedding:
                        embedding = llm.embed(obj["page_content"])
                        obj["embedding"] = embedding
                        usage = embedding.usage
                        total_usage += usage

                    out_f.write(json_dumps(obj) + "\n")

                    # Display progress on a single line
                    progress = (i + 1) / total_lines * 100
                    console.print(
                        f"진행률: {progress:.1f}% ({i+1}/{total_lines}) - 토큰: {total_usage.input}",
                        end="\r",
                    )

        # Display completion message
        console.print("\n")
        console.print("[green]임베딩 완료![/green]")
        console.print(f"출력 파일 생성됨: {jsonl_out_path}")
        console.print(f"총 항목 수: {total_lines}")
        console.print(f"총 토큰 수: {total_usage.input}")
    except (IOError, JSONDecodeError) as e:
        console.print(f"[red]파일 읽기 오류: {e}[/red]")
        raise typer.Exit(1)
