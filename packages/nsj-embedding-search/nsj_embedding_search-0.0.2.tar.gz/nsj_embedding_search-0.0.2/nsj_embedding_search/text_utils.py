import tiktoken

from nsj_embedding_search.settings import OPENAI_EMBEDDING_MODEL, logger


class TextUtils:

    def slip_text(
        self,
        content: str,
        chunck_size: int,
    ) -> tuple[list[str], list[str]]:
        """
        Quebra o texto da entrada "content" em partes cujo comprimento não exceda,
        em quantidade de tokens, o parâmetro chunck_size.

        Retorna uma tupla de duas listas de string:
        - Primeira: Lista de strings com overlap de metade do tamanho das partes.
        - Segunda: Lista de strings sem overlaop (só com o texto das partes quebradas).
        """

        # Verificando se estoura o limite de tokens de cada parte
        if self.count_tokens(content, OPENAI_EMBEDDING_MODEL) <= chunck_size:
            return ([content], [content])

        pieces = []
        pieces_overlap = []
        words = content.split()
        buffer = []
        buffer_overlap = []
        buffer_pendente = False
        for word in words:
            buffer_pendente = True
            buffer_overlap.append(word)
            buffer.append(word)

            # Começando um novo buffer, caso haja estouro do limite
            if (
                self.count_tokens(" ".join(buffer_overlap), OPENAI_EMBEDDING_MODEL)
                >= chunck_size
            ):
                pieces_overlap.append(" ".join(buffer_overlap[:-1]))
                pieces.append(" ".join(buffer[:-1]))

                buffer_overlap = buffer_overlap[
                    (-1 * int(len(buffer_overlap) / 2) - 1) :
                ]
                buffer = buffer[-1:]

                buffer_pendente = False

                # Garantindo que o próximo buffer não nasce já estourando o limite
                while (
                    self.count_tokens(" ".join(buffer_overlap), OPENAI_EMBEDDING_MODEL)
                    >= chunck_size
                ):
                    if len(buffer_overlap) <= 1:
                        logger.warning(
                            f"Não é possível quebrar este texto em partes com no máximo {chunck_size} tokens. Uma parte do texto será truncada em 100 caracteres (para caber)."
                        )
                        buffer_overlap[0] = buffer_overlap[0][:100]
                        buffer[0] = buffer[0][:100]
                        break

                    buffer_overlap = buffer_overlap[1:]

        if buffer_pendente:
            pieces_overlap.append(" ".join(buffer_overlap))
            pieces.append(" ".join(buffer))

        return (pieces_overlap, pieces)

    def count_tokens(self, text: str, model: str = OPENAI_EMBEDDING_MODEL) -> int:
        """Retorna o  número de tokens numa string."""
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
