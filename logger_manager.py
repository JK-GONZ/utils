'''
  Author: Jorge E. González Gonzalo
  Date: 2025-05-23
  GitHub: https://github.com/JK-GONZ

  Information:
    This file define a class to handle loggers in python
'''

# Import
import os
import logging
from logging.handlers import RotatingFileHandler


class OutputFilter(logging.Filter):
    '''
        Define el filtro que se aplicará en el logger
    '''
    def __init__(self, output_type: str):
        super().__init__()
        self.output_type = output_type  # 'console' o 'file'

    def filter(self, record: logging.LogRecord):
        # Añadimos un atributo personalizado en el registro
        return getattr(record, 'target', 'all') in (self.output_type, 'all')


class LoggerManager:
    '''
        Clase definida para facilitar la definición y el manejo
        de los loggers

        Parameters
        ----------
        level : str = 'INFO'
            Umbral minimo de severidad para que sea procesado
        log_to_file : bool = True
            Permite la escritura en archivo
        log_to_console : bool = True
            Permite la escritura en consola
        log_dir : str = '/logs'
            Define la ruta donde guardar los archivos
        filename : str = __name__
            Define el nombre del archivo .log
        max_file_size_mb : int = 5 
            Tamaño maximo del archivo antes de rotarlo
        backup_count : int = 3
            Cantidad maxima de ficheros que se guardarán de respaldo al rotar

        Usage
        -----
        logger = LoggerManager(
            name='main_log',
            level='DEBUG',
            log_to_console=False,
            filename='main_logdatamerger',
            log_dir='logs/prueba',
            max_file_size=20,
            backup_count=3
        )
    '''

    def __init__(self, name: str,
                 level: str = 'INFO',
                 log_to_file: bool = True,
                 log_to_console: bool = True,
                 log_dir: str = 'logs',
                 filename: str = __name__,
                 max_file_size: int = 1,
                 backup_count: int = 3):

        self.logger = logging.getLogger(name)
        self.logger.setLevel(self._get_level(level))
        self.logger.propagate = False

        if log_to_console and log_to_file:
            self.target = 'all'
        elif log_to_file:
            self.target = 'file'
        elif log_to_console:
            self.target = 'console'
        else:
            self.target = None

        self.max_bytes = max_file_size * 1024 * 1024
        self.max_file_size = max_file_size
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            '%Y-%m-%d %H:%M:%S'
        )

        if not log_to_console:
            pass
        else:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.addFilter(OutputFilter('console'))
            self.logger.addHandler(console_handler)

        if not log_to_file:
            pass
        else:
            os.makedirs(log_dir, exist_ok=True)
            if not filename:
                filename = f"{name}.log"
            file_path = os.path.join(log_dir, filename + '.log')

            file_handler = RotatingFileHandler(
                file_path, maxBytes=self.max_bytes, backupCount=backup_count
            )
            file_handler.setFormatter(formatter)
            file_handler.addFilter(OutputFilter('file'))
            self.logger.addHandler(file_handler)

    def _get_level(self, level_str: str):
        levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return levels.get(level_str.upper(), logging.INFO)

    def error(self, msg: str):
        """
        Enviar un log de tipo error
        """
        extra = {'target': self.target}
        self.logger.log(logging.ERROR, msg, extra=extra)


    def info(self, msg: str):
        """
        Enviar un log de tipo info
        """
        extra = {'target': self.target}
        self.logger.log(logging.INFO, msg, extra=extra)

    def debug(self, msg: str):
        """
        Enviar un log de tipo debug
        """
        extra = {'target': self.target}
        self.logger.log(logging.DEBUG, msg, extra=extra)


    def critical(self, msg: str):
        """
        Enviar un log de tipo critical
        """
        extra = {'target': self.target}
        self.logger.log(logging.CRITICAL, msg, extra=extra)


    def warning(self, msg: str):
        """
        Enviar un log de tipo warning
        """
        extra = {'target': self.target}
        self.logger.log(logging.WARNING, msg, extra=extra)


    def get_max_bytes(self):
        '''
            Return the max file size in bytes
        '''
        return self.max_bytes

    def get_max_file_size(self):
        '''
            Return the max file size in mb
        '''
        return self.max_file_size
