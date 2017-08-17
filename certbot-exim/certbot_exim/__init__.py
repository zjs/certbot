"""
The `~certbot_exim.installer` plugin automates the process of installing certificates for the Exim
mail transfer agent.

The plugin will configure Exim to use the certificate and private key managed by Certbot.

The plugin will enable STARTTLS and set required ciphers based on Mozilla recommendations.


Named Arguments
---------------

=============================  ==========================================================
``--exim-server-root``         The Exim server's root directory (Default: ``/etc/exim4``)
``--exim-file-configuration``  ``single-file`` to indicate a single file is used for
                               configuration or ``split-file`` to indicate that a
                               configuration directory is used.
=============================  ==========================================================


Supported Enhancements
----------------------

=============================  ==========================================================
``--staple-ocsp``              Enables OCSP Stapling. A valid OCSP response is
                               stapled to the certificate that the server offers
                               during TLS. (default: None)
=============================  ==========================================================


Examples
--------

.. code-block:: bash
   :caption: To acquire a certificate for ``example.com`` using the ``standalone`` plugin to
             complete a ``http-01`` challenge, configure Exim to use it, and enable OCSP stapling.

   certbot --exim \\
     --standalone \\
     --staple-ocsp \\
     -d example.com

.. code-block:: bash
   :caption: To acquire a certificate for ``example.com`` using the ``standalone`` plugin to
             complete a ``http-01`` challenge and configure Exim to use it following the split-file
            pattern, without enabling OCSP stapling.

   certbot --exim \\
     --standalone \\
     --exim-file-configuration=split-file \\
     -d example.com

.. code-block:: bash
   :caption: To acquire a certificate for ``example.com`` using the ``dns-cloudflare`` plugin to
             complete a ``dns-01`` challenge and configure Exim to use it, without enabling OCSP
             stapling.

   certbot --exim \\
     --dns-cloudflare \\
     --dns-cloudflare-credentials ~/.secrets/certbot/cloudflare.ini \\
     -d example.com
"""
