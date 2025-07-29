from abc import ABC, abstractmethod
import pandas as pd


class AbstractParser(ABC):
    @abstractmethod
    def parse_flashscore(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def parse_isdb(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

