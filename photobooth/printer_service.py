from __future__ import annotations

import logging
from pathlib import Path
from tempfile import NamedTemporaryFile

from PIL import Image, ImageOps
from escpos.printer import Usb

import config


logger = logging.getLogger(__name__)


class PrinterService:
    def __init__(self) -> None:
        self.enabled = config.PRINTER_ENABLED

    def _create_printer(self) -> Usb:
        """
        Cria uma nova conexão USB com a impressora.

        Criamos a conexão somente no momento da impressão para reduzir
        problemas de conexão USB mantida aberta por muito tempo.
        """
        return Usb(
            config.PRINTER_VENDOR_ID,
            config.PRINTER_PRODUCT_ID,
            in_ep=config.PRINTER_IN_ENDPOINT,
            out_ep=config.PRINTER_OUT_ENDPOINT,
        )

    def _prepare_image(self, image_path: Path) -> Path:
        """
        Prepara a foto para impressão térmica:
        - corrige orientação EXIF;
        - converte para escala de cinza;
        - redimensiona para a largura da impressora;
        - mantém a proporção original;
        - aumenta levemente o contraste;
        - salva uma imagem temporária.
        """
        with Image.open(image_path) as source_image:
            image = ImageOps.exif_transpose(source_image)
            image = image.convert("L")

            target_width = config.PRINTER_IMAGE_WIDTH

            if image.width != target_width:
                scale = target_width / image.width
                target_height = max(1, round(image.height * scale))

                image = image.resize(
                    (target_width, target_height),
                    Image.Resampling.LANCZOS,
                )

            image = ImageOps.autocontrast(image)

            temporary_file = NamedTemporaryFile(
                suffix=".png",
                delete=False,
            )
            temporary_path = Path(temporary_file.name)
            temporary_file.close()

            image.save(temporary_path, format="PNG")

        return temporary_path

    def print_photo(self, image_path: str | Path) -> bool:
        """
        Imprime uma fotografia salva.

        Retorna True quando o comando de impressão é enviado com sucesso.
        Lança uma exceção quando ocorre erro, permitindo que a interface
        exiba uma mensagem e ofereça uma nova tentativa.
        """
        if not self.enabled:
            logger.info("Impressão desabilitada no config.py.")
            return True

        photo_path = Path(image_path)

        if not photo_path.exists():
            raise FileNotFoundError(
                f"A fotografia não foi encontrada: {photo_path}"
            )

        temporary_path: Path | None = None
        printer: Usb | None = None

        try:
            temporary_path = self._prepare_image(photo_path)
            printer = self._create_printer()

            printer.set(
                align="center",
                bold=False,
                width=1,
                height=1,
            )

            printer.image(str(temporary_path))

            # Avança um pouco o papel antes do corte.
            printer.text("\n\n\n")

            if config.PRINTER_CUT_AFTER_PRINT:
                printer.cut()

            logger.info("Foto enviada para impressão: %s", photo_path)
            return True

        except Exception:
            logger.exception(
                "Falha ao imprimir a fotografia: %s",
                photo_path,
            )
            raise

        finally:
            if printer is not None:
                try:
                    printer.close()
                except Exception:
                    logger.debug(
                        "Não foi possível fechar a conexão da impressora.",
                        exc_info=True,
                    )

            if temporary_path is not None:
                try:
                    temporary_path.unlink(missing_ok=True)
                except OSError:
                    logger.debug(
                        "Não foi possível apagar a imagem temporária.",
                        exc_info=True,
                    )
