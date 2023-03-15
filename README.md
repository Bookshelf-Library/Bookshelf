<h1 align="center">Bookshelf</h1>

<h2 align="center"><i>Levando a leitura para além dos limites</i></h2>

<br/>

<p>A Bookshelf é uma aplicação que veio para simplificar os empréstimos de livros, basta entrar em contato com seu colaborador para que o empréstimo seja feito!</p>

<p>Com processos <b>simples</b>, você estudante pode consultar seus prazos de entrega, visualizar os livros disponíveis, e o melhor de tudo, ao demosntrar interesse seguindo um livro, <strong>receberá um email assim que uma cópia dele estiver disponível!</strong><p>

<br/>
<br/>

<h2 align="center">Iniciando a aplicação</h2>

<br/>

<p>Primeiro, é necessário criar um ambiente virtual para poder instalar os pacotes. Pode ser feito da seguinte forma no terminal aberto no diretório do projeto:</p>

<br/>

```Bash
python -m venv venv
```

<blockquote>Obs: o segundo "venv" é o nome da pasta que deseja criar para a instalação dos pacotes, porém por boas práticas aconselhamos manter dessa forma!</blockquote>

<br/>

<p>Uma vez que a pasta já foi criada, basta rodar o seguinte comando para entrar o ambiente virtual</p>

<br/>

- Linux

```Bash
source venv/bin/activate
```

<br/>

- Windows

<p>Comando para verificação de entrada no ambiente virtual:</p>

```Bash
Get-ExecutionPolicy
```

<p>Caso o retorno seja "Restricted", basta inserir o seguinte código:</p>

```Bash
Set-ExecutionPolicy AllSigned
```

<p>Digite "S" ou "Y" para confirmar</p>

<br/>

<p>Após esse processo, basta inserir o seguinte comando:</p>

```Bash
.\venv\Scripts\activate
```

<br/>

<blockquote>Obs: caso esteja utilizando o bash do Git, o comando para ativar o ambiente virtual é o seguinte:</blockquote>

<br/>

```Bash
source venv/Scripts/activate
```

<p>Agora que o ambiente virtual está criado e já entramos nele, basta rodar o seguinte comando para instalar as dependências:</p>

```Bash
pip intall -r requirements.txt
```

<br/>

<h2 align="center">Rodando o projeto</h2>

<p>Uma vez que as dependências do projeto foram instaladas de forma correta, para rodar o projeto localmente basta rodar o seguinte comando:</p>

```Bash
python manage.py runserver
```

<br/>

<details>
    <summary align="center">Principais tecnologias utilizadas no projeto:</summary>
    <ul>
        <li>python</li>
        <li>django</li>
        <li>djangorestframework</li>
        <li>djangorestframework-simplejwt</li>
        <li>psycopg2-binary</li>
        <li>python-dotenv</li>
    </ul>
</details>
