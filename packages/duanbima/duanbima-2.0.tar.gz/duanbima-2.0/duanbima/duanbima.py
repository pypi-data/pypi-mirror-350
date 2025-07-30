import datetime
import calendar
import importlib.resources # Adicione esta linha
# import sys # Pode ser útil para depurar caminhos de recursos

# Global set to store non-business days from ANBIMA calendar
_anbima_non_business_days = set()
_holidays_loaded = False
# Nome do arquivo de feriados padrão dentro do pacote
_default_holiday_file_name = "anbima_holidays.txt"
# Caminho para um arquivo de feriados externo configurado pelo usuário
_external_holiday_file_path = None

def _parse_date_input(date_input) -> datetime.date:
    """
    Converte uma entrada (string ou datetime.date) para um objeto datetime.date.
    Suporta strings nos formatos "YYYY-MM-DD" e "DD/MM/YYYY".

    Args:
        date_input: A data a ser convertida (str ou datetime.date).

    Returns:
        datetime.date: O objeto de data correspondente.

    Raises:
        TypeError: Se o tipo de entrada não for suportado.
        ValueError: Se a string de data não puder ser parseada.
    """
    if isinstance(date_input, datetime.date):
        return date_input
    if isinstance(date_input, str):
        try:
            # Tentar formato YYYY-MM-DD
            return datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            try:
                # Tentar formato DD/MM/YYYY
                return datetime.datetime.strptime(date_input, "%d/%m/%Y").date()
            except ValueError:
                raise ValueError(f"Formato de data inválido para '{date_input}'. Use YYYY-MM-DD, DD/MM/YYYY ou um objeto datetime.date.")
    raise TypeError("Entrada de data deve ser um objeto datetime.date ou uma string (YYYY-MM-DD, DD/MM/YYYY).")


def configurar_arquivo_feriados(caminho_arquivo: str):
    """
    Configura o caminho para um arquivo .txt externo contendo os dias não úteis.
    Este arquivo deve conter uma data por linha, nos formatos "YYYY-MM-DD" ou DD/MM/YYYY.

    Args:
        caminho_arquivo (str): O caminho completo para o arquivo de feriados externo.
                               Isso fará com que a biblioteca use este arquivo em vez
                               do arquivo padrão empacotado.
    """
    global _external_holiday_file_path, _holidays_loaded, _anbima_non_business_days
    _external_holiday_file_path = caminho_arquivo # Armazena o caminho externo
    _anbima_non_business_days = set() # Resetar feriados anteriores
    _holidays_loaded = False # Forçar recarregamento na próxima necessidade


def _load_holidays():
    """
    Carrega os dias não úteis do arquivo configurado (externo) ou do pacote (padrão).
    """
    global _anbima_non_business_days, _holidays_loaded, _default_holiday_file_name, _external_holiday_file_path
    if _holidays_loaded:
        return

    # Preferência: se um caminho externo foi configurado, use-o
    if _external_holiday_file_path:
        try:
            with open(_external_holiday_file_path, 'r', encoding='utf-8') as f:
                for line_number, line in enumerate(f, 1):
                    date_str = line.strip()
                    if not date_str:
                        continue

                    parsed_date = None
                    try:
                        parsed_date = _parse_date_input(date_str)
                    except (ValueError, TypeError):
                        print(f"Aviso: Formato de data inválido ou tipo incorreto na linha {line_number} do arquivo '{_external_holiday_file_path}': '{date_str}'.")
                    
                    if parsed_date:
                        _anbima_non_business_days.add(parsed_date)
            _holidays_loaded = True
            return # Carregamento bem-sucedido do arquivo externo
        except FileNotFoundError:
            print(f"Aviso: Arquivo de feriados configurado '{_external_holiday_file_path}' não encontrado. Tentando carregar o arquivo padrão do pacote (se existir).")
        except Exception as e:
            print(f"Erro ao carregar arquivo de feriados externo '{_external_holiday_file_path}': {e}. Tentando carregar o arquivo padrão do pacote.")

    # Se não há caminho externo ou falhou, tenta carregar o arquivo padrão do pacote
    try:
        # Use importlib.resources.files para obter um objeto Path que pode ser aberto
        # 'duanbima' é o nome do seu pacote, '_default_holiday_file_name' é o nome do arquivo.
        resource_path = importlib.resources.files('duanbima').joinpath(_default_holiday_file_name)
        with resource_path.open('r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, 1):
                date_str = line.strip()
                if not date_str:
                    continue

                parsed_date = None
                try:
                    parsed_date = _parse_date_input(date_str)
                except (ValueError, TypeError):
                    print(f"Aviso: Formato de data inválido ou tipo incorreto na linha {line_number} do arquivo de feriados '{_default_holiday_file_name}' dentro do pacote: '{date_str}'.")
                
                if parsed_date:
                    _anbima_non_business_days.add(parsed_date)
        _holidays_loaded = True

    except FileNotFoundError:
        print(f"Aviso: Arquivo de feriados padrão '{_default_holiday_file_name}' não encontrado no pacote 'duanbima'. Os cálculos de dias úteis considerarão apenas fins de semana.")
    except Exception as e:
        print(f"Erro ao carregar arquivo de feriados do pacote '{_default_holiday_file_name}': {e}")


def _ensure_holidays_loaded():
    """Garante que os feriados foram carregados."""
    if not _holidays_loaded:
        _load_holidays()


def is_business_day(date_obj: datetime.date) -> bool:
    """
    Verifica se uma data específica é um dia útil.
    Um dia útil não é sábado, domingo ou um feriado ANBIMA.

    Args:
        date_obj (datetime.date): A data para verificar.

    Returns:
        bool: True se for um dia útil, False caso contrário.
    """
    _ensure_holidays_loaded()
    if not isinstance(date_obj, datetime.date):
        raise TypeError("is_business_day espera um objeto datetime.date.")
        
    # Verifica se é fim de semana (Segunda-feira=0, Domingo=6)
    if date_obj.weekday() >= 5:  # Sábado ou Domingo
        return False
    # Verifica se está na lista de dias não úteis da ANBIMA
    if date_obj in _anbima_non_business_days:
        return False
    return True


def _get_next_business_day(date_obj: datetime.date) -> datetime.date:
    """Retorna o próximo dia útil a partir da data fornecida (exclusive)."""
    next_day = date_obj + datetime.timedelta(days=1)
    while not is_business_day(next_day):
        next_day += datetime.timedelta(days=1)
    return next_day


def _get_previous_business_day(date_obj: datetime.date) -> datetime.date:
    """Retorna o dia útil anterior a partir da data fornecida (exclusive)."""
    prev_day = date_obj - datetime.timedelta(days=1)
    while not is_business_day(prev_day):
        prev_day -= datetime.timedelta(days=1)
    return prev_day


def hoje(offset: int = 0) -> datetime.date:
    """
    Retorna um dia útil com base na data atual, ajustado por um offset.
    Se a data atual não for um dia útil, a base para o cálculo é o próximo dia útil.

    Args:
        offset (int, optional): O número de dias úteis para avançar (positivo)
                                ou retroceder (negativo). Padrão é 0.

    Returns:
        datetime.date: O objeto de data do dia útil calculado.
    """
    _ensure_holidays_loaded()
    current_actual_date = datetime.date.today()

    base_bday = current_actual_date
    if not is_business_day(base_bday):
        base_bday = _get_next_business_day(base_bday)

    target_bday = base_bday
    if offset > 0:
        for _ in range(offset):
            target_bday = _get_next_business_day(target_bday)
    elif offset < 0:
        for _ in range(abs(offset)):
            target_bday = _get_previous_business_day(target_bday)
            
    return target_bday


def ultimodu(year: int, month: int) -> datetime.date:
    """
    Retorna o último dia útil de um determinado mês e ano.

    Args:
        year (int): O ano.
        month (int): O mês (1-12).

    Returns:
        datetime.date: O objeto de data do último dia útil do mês.

    Raises:
        ValueError: Se o ano ou mês não forem inteiros válidos, ou se o mês
                    estiver fora do intervalo 1-12.
        Exception: Se nenhum dia útil for encontrado no mês especificado.
    """
    _ensure_holidays_loaded()
    try:
        year_int = int(year)
        month_int = int(month)
    except ValueError:
        raise ValueError("Ano e mês devem ser valores inteiros ou conversíveis para inteiros.")

    if not (1 <= month_int <= 12):
        raise ValueError("Mês deve estar entre 1 e 12.")

    _, num_days_in_month = calendar.monthrange(year_int, month_int)
    
    last_calendar_day_of_month = datetime.date(year_int, month_int, num_days_in_month)
    
    current_date_to_check = last_calendar_day_of_month
    while not is_business_day(current_date_to_check):
        current_date_to_check -= datetime.timedelta(days=1)
        if current_date_to_check.month != month_int:
            # Chegou ao mês anterior sem encontrar dia útil, o que é um caso extremo
            # e indica que o mês não possui dias úteis (muito improvável para um mês real)
            raise Exception(f"Não foi possível encontrar um dia útil para {month_int:02d}/{year_int}.")
            
    return current_date_to_check


def mes(offset: int = 0) -> int:
    """
    Retorna o número do mês com base no mês atual, ajustado por um offset.

    Args:
        offset (int, optional): O número de meses para avançar (positivo)
                                ou retroceder (negativo). Padrão é 0.

    Returns:
        int: O número do mês (1-12).
    """
    today_date = datetime.date.today()
    current_month_val = today_date.month
    current_year_val = today_date.year

    total_months_from_epoch = current_year_val * 12 + (current_month_val - 1)
    target_total_months = total_months_from_epoch + offset
    
    target_month_zero_based = target_total_months % 12
    return target_month_zero_based + 1


def ano(offset: int = 0) -> int:
    """
    Retorna o ano com base no ano atual, ajustado por um offset.

    Args:
        offset (int, optional): O número de anos para avançar (positivo)
                                ou retroceder (negativo). Padrão é 0.

    Returns:
        int: O número do ano.
    """
    today_date = datetime.date.today()
    current_year_val = today_date.year
    return current_year_val + offset


def qtdu(data_inicio, data_fim) -> int:
    """
    Conta a quantidade de dias úteis entre data_inicio e data_fim (ambas inclusivas).
    As datas podem ser objetos datetime.date ou strings ("YYYY-MM-DD" ou "DD/MM/YYYY").

    Args:
        data_inicio: A data de início do período (datetime.date ou str).
        data_fim: A data de fim do período (datetime.date ou str).

    Returns:
        int: A quantidade de dias úteis no intervalo. Retorna 0 se data_inicio > data_fim.

    Raises:
        TypeError: Se as entradas de data não forem datetime.date ou string.
        ValueError: Se as strings de data não puderem ser parseadas.
    """
    _ensure_holidays_loaded()
    
    start_date = _parse_date_input(data_inicio)
    end_date = _parse_date_input(data_fim)

    if start_date > end_date:
        return 0

    count = 0
    current_date_iter = start_date
    while current_date_iter <= end_date:
        if is_business_day(current_date_iter):
            count += 1
        # Verificação de segurança para evitar loop infinito em caso de erro lógico extremo
        if (current_date_iter - start_date).days > (366 * 10) and (end_date - start_date).days > (366*10): # Ex: limite de 10 anos
            raise OverflowError("Intervalo de datas excessivamente grande ou loop inesperado.")
        current_date_iter += datetime.timedelta(days=1)
    return count


def contadu(year: int, month: int, n_th: int) -> datetime.date:
    """
    Retorna o n-ésimo dia útil de um determinado mês e ano.

    Args:
        year (int): O ano.
        month (int): O mês (1-12).
        n_th (int): O n-ésimo dia útil desejado (ex: 1 para o primeiro, 5 para o quinto).
                    Deve ser >= 1.

    Returns:
        datetime.date: O objeto de data do n-ésimo dia útil.

    Raises:
        ValueError: Se os parâmetros não forem inteiros válidos, se o mês estiver
                    fora do intervalo 1-12, se n_th < 1, ou se o mês não
                    possuir n_th dias úteis.
    """
    _ensure_holidays_loaded()
    try:
        year_int = int(year)
        month_int = int(month)
        n_th_int = int(n_th)
    except ValueError:
        raise ValueError("Ano, mês e n (n-ésimo dia) devem ser valores inteiros.")

    if not (1 <= month_int <= 12):
        raise ValueError("Mês deve estar entre 1 e 12.")
    if n_th_int < 1:
        raise ValueError("O n-ésimo dia útil (n_th) deve ser maior ou igual a 1.")

    current_date = datetime.date(year_int, month_int, 1)
    business_days_found_count = 0

    while current_date.month == month_int:
        if is_business_day(current_date):
            business_days_found_count += 1
            if business_days_found_count == n_th_int:
                return current_date
        current_date += datetime.timedelta(days=1)
        # Medida de segurança para evitar loop infinito se algo estiver muito errado
        if current_date > datetime.date(year_int, month_int, 1) + datetime.timedelta(days=40):
            # (um mês nunca terá mais de 31 dias + alguns dias para buffer)
            break 
            
    # Se saiu do loop e não retornou, o n-ésimo dia útil não foi encontrado
    raise ValueError(f"O mês {month_int:02d}/{year_int} não possui {n_th_int} dias úteis.")


def help():
    """
    Mostra uma mensagem de ajuda com a descrição das funções da biblioteca duanbima.
    """
    help_text = f"""
===============================================================================
 Biblioteca duanbima - Funções para Dias Úteis (Calendário ANBIMA)
===============================================================================
 Autor: Lucas Soares
 Email: lcs-soares@hotmail.com
 Versão: 1.2 (Adicionada contadu)

 Descrição:
 Esta biblioteca fornece funções para cálculos envolvendo dias úteis,
 com base em fins de semana e um arquivo de feriados personalizável.

-------------------------------------------------------------------------------
 Funções disponíveis:
-------------------------------------------------------------------------------

1. configurar_arquivo_feriados(caminho_arquivo: str)
   Configura o caminho para um arquivo .txt externo contendo os dias não úteis.
   Se não for chamado, a biblioteca tentará carregar '{_default_holiday_file_name}'
   empacotado com a própria biblioteca.
   O arquivo deve ter uma data por linha (YYYY-MM-DD ou DD/MM/YYYY).
   Ex: duanbima.configurar_arquivo_feriados("meus_feriados.txt")

2. hoje(offset: int = 0) -> datetime.date
   Retorna um dia útil com base na data atual, ajustado por um offset de
   dias úteis. Se a data atual não for útil, a base para o cálculo é o
   próximo dia útil.
   - offset > 0: avança N dias úteis.
   - offset < 0: retrocede N dias úteis.
   - offset = 0 (padrão): dia útil de referência (hoje ou próximo útil).
   Ex: dia_util_hoje = duanbima.hoje()
       proximo_dia_util = duanbima.hoje(1)
       dia_util_anterior = duanbima.hoje(-1)

3. ultimodu(year: int, month: int) -> datetime.date
   Retorna o último dia útil de um determinado mês e ano.
   `year` e `month` devem ser inteiros.
   Ex: ultimo_du_abril_2025 = duanbima.ultimodu(2025, 4)

4. mes(offset: int = 0) -> int
   Retorna o número do mês (1-12) com base no mês atual, ajustado por um
   offset de meses.
   Ex: mes_atual = duanbima.mes()
       mes_anterior = duanbima.mes(-1) # Retorna 12 se o atual for 1

5. ano(offset: int = 0) -> int
   Retorna o número do ano com base no ano atual, ajustado por um offset
   de anos.
   Ex: ano_atual = duanbima.ano()
       ano_seguinte = duanbima.ano(1)

6. qtdu(data_inicio, data_fim) -> int
   Conta a quantidade de dias úteis entre `data_inicio` e `data_fim`
   (ambas as datas são inclusivas na contagem).
   As datas podem ser objetos datetime.date ou strings ("YYYY-MM-DD" ou "DD/MM/YYYY").
   Retorna 0 se data_inicio > data_fim.
   Ex: dias_uteis = duanbima.qtdu(datetime.date(2024, 1, 1), "31/01/2024")

7. contadu(year: int, month: int, n_th: int) -> datetime.date
   Retorna o n-ésimo dia útil de um determinado mês e ano.
   `year`, `month` e `n_th` (o n-ésimo dia útil desejado, ex: 5 para o quinto)
   devem ser inteiros. `n_th` deve ser >= 1.
   Levanta ValueError se o mês não tiver 'n_th' dias úteis.
   Ex: quinto_dia_util = duanbima.contadu(2025, 4, 5)

8. help()
   Mostra esta mensagem de ajuda detalhada.

-------------------------------------------------------------------------------
 Arquivo de Feriados:
 - Por padrão, a biblioteca tenta carregar um arquivo chamado '{_default_holiday_file_name}'
   que deve ser **empacotado junto com a biblioteca** (dentro da pasta 'duanbima').
 - Você pode configurar um caminho externo para um arquivo de feriados usando
   `configurar_arquivo_feriados()`. Isso é útil se você quiser usar uma lista
   de feriados diferente da que vem com a biblioteca ou se ela for dinâmica.
 - Crie este arquivo com uma data não útil por linha (formatos: YYYY-MM-DD
   ou DD/MM/YYYY). Exemplo:
      2025-01-01
      25/12/2025
===============================================================================
    """
    print(help_text)