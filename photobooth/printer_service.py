from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from PIL import Image, ImageOps
from escpos.printer import Usb


@dataclass(frozen=True)
class PrintResult:
    success: bool
    message: str


class PrinterService:
    """
    Serviço responsável por preparar e imprimir as fotografias.

    Modos disponíveis:

    disabled:
        Apenas confirma que a fotografia foi salva.

    usb:
        Imprime diretamente em uma impressora ESC/POS conectada
        por USB usando python-escpos.
    """

    def __init__(
        self,
        mode: str = "disabled",
        vendor_id: Optional[int] = None,
        product_id: Optional[int] = None,
        in_endpoint: Optional[int] = None,
        out_endpoint: Optional[int] = None,
        image_width: int = 384,
        feed_lines: int = 3,
        cut_after_print: bool = True,
    ) -> None:
        normalized_mode = mode.strip().lower()

        if normalized_mode not in {"disabled", "usb"}:
            raise ValueError(
                'Modo de impressão inválido. Use "disabled" ou "usb".'
            )

        if image_width <= 0:
            raise ValueError(
                "A largura da imagem da impressora deve ser maior que zero."
            )

        if feed_lines < 0:
            raise ValueError(
                "A quantidade de linhas de avanço não pode ser negativa."
            )

        if normalized_mode == "usb":
            if vendor_id is None:
                raise ValueError("PRINTER_VENDOR_ID não foi configurado.")

            if product_id is None:
                raise ValueError("PRINTER_PRODUCT_ID não foi configurado.")

        self.mode = normalized_mode
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.in_endpoint = in_endpoint
        self.out_endpoint = out_endpoint
        self.image_width = image_width
        self.feed_lines = feed_lines
        self.cut_after_print = cut_after_print

    @property
    def enabled(self) -> bool:
        return self.mode == "usb"

    def _create_printer(self) -> Usb:
        printer_arguments = {
            "idVendor": self.vendor_id,
            "idProduct": self.product_id,
        }

        if self.in_endpoint is not None:
            printer_arguments["in_ep"] = self.in_endpoint

        if self.out_endpoint is not None:
            printer_arguments["out_ep"] = self.out_endpoint

        return Usb(**printer_arguments)

    def _prepare_image(self, photo_path: Path) -> Image.Image:
        """
        Carrega e prepara a fotografia para a largura da impressora.

        A imagem:
        - tem sua orientação EXIF corrigida;
        - é convertida para escala de cinza;
        - é redimensionada sem deformação;
        - recebe ajuste automático de contraste.
        """
        with Image.open(photo_path) as source:
            image = ImageOps.exif_transpose(source)
            image = image.convert("L")

            if image.width != self.image_width:
                scale = self.image_width / image.width
                target_height = max(
                    1,
                    round(image.height * scale),
                )

                image = image.resize(
                    (self.image_width, target_height),
                    Image.Resampling.LANCZOS,
                )

            image = ImageOps.autocontrast(image)

            # Retorna uma cópia independente porque o arquivo será fechado
            # ao sair do bloco with.
            return image.copy()

    def process_photo(self, photo_path: Path) -> PrintResult:
        photo_path = Path(photo_path)

        if not photo_path.exists():
            return PrintResult(
                False,
                f"Arquivo não encontrado: {photo_path}",
            )

        if self.mode == "disabled":
            return PrintResult(
                True,
                f"Foto salva em {photo_path.name}. Impressão desativada.",
            )

        printer: Optional[Usb] = None

        try:
            image = self._prepare_image(photo_path)
            printer = self._create_printer()

            printer.set(
                align="center",
                bold=False,
                width=1,
                height=1,
            )

            printer.image(image)

            if self.feed_lines > 0:
                printer.text("\n" * self.feed_lines)

            if self.cut_after_print:
                printer.cut()

            return PrintResult(
                True,
                "Foto impressa com sucesso.",
            )

        except Exception as error:
            return PrintResult(
                False,
                f"Não foi possível imprimir a foto: {error}",
            )

        finally:
            if printer is not None:
                try:
                    printer.close()
                except Exception:
                    pass
