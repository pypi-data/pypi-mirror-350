import json
from pathlib import Path
from typing import Any, Dict


class Lang:
    def __init__(self, locales_dir: Path, default_lang: str = "en-US"):
        self.locales: Dict[str, Dict[str, Any]] = {}
        self.default_lang = default_lang
        self._load_locales(locales_dir)

    def _load_locales(self, locales_dir: Path):
        """Carrega todos os arquivos de localização"""
        for file in locales_dir.glob("*.json"):
            lang_code = file.stem  # Obtém o código do idioma do nome do arquivo
            with open(file, "r", encoding="utf-8") as f:
                self.locales[lang_code] = json.load(f)
            print(f"|-- Locale loaded: {lang_code}")

    def get(self, key: str, locale: str = "", **kwargs) -> str:
        """
        Obtém uma tradução para a chave especificada

        Args:
            key: Chave de tradução (ex: 'commands.ping.description')
            locale: Código de idioma (ex: 'pt-BR', 'en-US')
            kwargs: Parâmetros para formatação

        Returns:
            String traduzida ou a chave entre colchetes se não encontrada
        """
        locale = locale or self.default_lang
        messages = self._get_messages_for_locale(locale)

        try:
            # Navega pela estrutura de chaves
            value = messages
            for k in key.split("."):
                value = value[k]

            return value.format(**kwargs) if isinstance(value, str) else str(value)
        except (KeyError, TypeError, AttributeError):
            # Fallback para o idioma padrão se diferente
            if locale != self.default_lang:
                return self.get(key, self.default_lang, **kwargs)
            return f"[{key}]"  # Fallback final

    def _get_messages_for_locale(self, locale: str) -> Dict[str, Any]:
        """Obtém as mensagens para um locale específico"""
        # Tenta o locale exato primeiro
        if locale in self.locales:
            return self.locales[locale]

        # Tenta encontrar um locale similar (ex: 'pt' para 'pt-BR')
        base_lang = locale.split("-")[0]
        for lang_code in self.locales:
            if lang_code.split("-")[0] == base_lang:
                return self.locales[lang_code]

        return self.locales.get(self.default_lang, {})
