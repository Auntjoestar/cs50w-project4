# cs50w-project4
## Descripción
El proyecto consiste en recrear un aplicación como twitter donde el usuario pueda subir sus post, ver los post de otros usuarios, dar like, entre otras funciones.
## Particularidades
Para el siguiente proyecto he decidido hacer, en su mayoría, una SPA, por lo cual casi todos los aspectos están controlados por medio de la fetch API de JavaScript.
## Perfil
Como funcionalidad extra he decidido implementar la opción que el usuario pueda subir foto de perfil, por lo cual esa es la única parte que está controlado meramente por medio de una view, pues no logré subir la foto por medio de un fetch.
## Post
El usuario puede hacer un post desde el apartado de index, como este está controlado por jscript no hay necesidad de recargar la página. 
## Ver posts
El usuario tiene dos apartados, uno para los post generales y otro para los post de personas que ellos siguen, ambos apartados cuentan de páginación combinando el paginator de Django y funciones de jscript. Del mismo modo, la paginación está límitada 10 post por página.
## Editar post
El usuario tiene la opción de editar un post, sin necesidad de recargar la página, dentro de la view hay una validación que si el usuario no es el que hizo el post, la petición fetch tire un fobidden.
## Likes
El usuario puede darle likes tanto a sus post, como a lo de los demás, no validé que el usuario no se pueda dar like a si mismo porque en la mayotía de redes sociales es permitido.
## Follow 
El usuario puede seguir y dejar de seguir a otro usuario sin necesidad de recargar la página, pues la vista será controlada a tiempo real con js.
## Login
Si el usuario intenta utilizar alguna de las funciones como subir un post y no está loggeado, le saldrá un mensaje de error para redirigirlo a la página de login. Las views están válidadas para que solo usuarios loggeados puedan interactuar.
