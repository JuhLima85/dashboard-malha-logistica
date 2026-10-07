IF DB_ID('CrossDockingDB') IS NULL
BEGIN
    CREATE DATABASE CrossDockingDB;
END
GO

USE CrossDockingDB;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.sequences
    WHERE name = 'SeqOperacaoForaCD'
)
BEGIN
    CREATE SEQUENCE SeqOperacaoForaCD
        AS INT
        START WITH 1
        INCREMENT BY 1;
END
GO

IF OBJECT_ID('dbo.OperacoesForaCD', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.OperacoesForaCD (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Codigo VARCHAR(30) NOT NULL UNIQUE,
        NumeroNota VARCHAR(50) NOT NULL,
        ValorNota DECIMAL(18,2) NOT NULL,
        Cliente VARCHAR(150) NOT NULL,
        Origem VARCHAR(100) NOT NULL,
        Destino VARCHAR(100) NOT NULL,
        TipoOperacao VARCHAR(100) NOT NULL,
        DataRecebimento DATE NOT NULL,
        StatusOperacao VARCHAR(30) NOT NULL
            CONSTRAINT DF_OperacoesForaCD_Status DEFAULT ('Em trânsito'),
        Placa VARCHAR(10) NULL,
        Motorista VARCHAR(150) NULL,
        DataEntrega DATETIME2 NULL,
        DataCadastro DATETIME2 NOT NULL
            CONSTRAINT DF_OperacoesForaCD_DataCadastro DEFAULT (SYSDATETIME()),
        DataAtualizacao DATETIME2 NOT NULL
            CONSTRAINT DF_OperacoesForaCD_DataAtualizacao DEFAULT (SYSDATETIME()),

        CONSTRAINT CK_OperacoesForaCD_Status
            CHECK (StatusOperacao IN ('Em trânsito', 'Entregue'))
    );
END
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE name = 'IX_OperacoesForaCD_NumeroNota'
      AND object_id = OBJECT_ID('dbo.OperacoesForaCD')
)
BEGIN
    CREATE INDEX IX_OperacoesForaCD_NumeroNota
        ON dbo.OperacoesForaCD (NumeroNota);
END
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE name = 'IX_OperacoesForaCD_Status'
      AND object_id = OBJECT_ID('dbo.OperacoesForaCD')
)
BEGIN
    CREATE INDEX IX_OperacoesForaCD_Status
        ON dbo.OperacoesForaCD (StatusOperacao);
END
GO
